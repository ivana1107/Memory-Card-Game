import pygame
import os
import random
from modules.game_configuration import MemoryCardGame

class Level:
    def setup_game(self, level, screen, bg_image, game_width, game_height, font, gray_color):
        """Configure game setup based on difficulty level."""
        self.screen = screen
        self.bg_image = bg_image
        self.game_width = game_width
        self.game_height = game_height
        self.font = font
        self.GRAY = gray_color

        # Initialize global variables
        self.memory_pictures = []
        for item in os.listdir('images'):
            self.memory_pictures.append(item.split('.')[0])

        # Define grid and bomb configuration
        self.rows, self.cols, self.num_bombs = {
            "easy": (3, 3, 1),  # 3x3 grid with 1 bomb
            "medium": (4, 4, 2),  # 4x4 grid with 2 bombs
            "hard": (5, 5, 3),  # 5x5 grid with 3 bombs
        }[level]

        self.num_pairs = (self.rows * self.cols - self.num_bombs) // 2

        # Ensure there are enough unique images for the selected level
        if self.num_pairs > len(self.memory_pictures):
            raise ValueError("Not enough unique images for the selected level.")

        # Dynamic card size and padding calculation
        self.grid_width = self.game_width - 150
        self.grid_height = self.game_height - 150
        self.pic_size = min(self.grid_width // self.cols, self.grid_height // self.rows) - 10  # Adjust with padding
        self.padding = 10
        self.left_margin = (self.game_width - (self.pic_size + self.padding) * self.cols + self.padding) // 2
        self.top_margin = (self.game_height - (self.pic_size + self.padding) * self.rows + self.padding) // 2

        # Select images for the game
        selected_images = random.sample(self.memory_pictures, self.num_pairs)
        selected_images *= 2  # Duplicate to make pairs
        selected_images += ["bomb"] * self.num_bombs
        random.shuffle(selected_images)

        # Reset global variables
        self.nem_pics = []
        self.nem_pics_rect = []
        self.hidden_images = []

        # Load images and set positions
        for item in selected_images:
            picture = pygame.image.load(f'images/{item}.png')
            picture = pygame.transform.scale(picture, (self.pic_size, self.pic_size))
            self.nem_pics.append(picture)
            picture_rect = picture.get_rect()
            self.nem_pics_rect.append(picture_rect)

        for i in range(len(self.nem_pics_rect)):
            self.nem_pics_rect[i][0] = self.left_margin + ((self.pic_size + self.padding) * (i % self.cols))
            self.nem_pics_rect[i][1] = self.top_margin + ((self.pic_size + self.padding) * (i // self.cols))
            self.hidden_images.append(False)

        return self.nem_pics, self.nem_pics_rect, selected_images, self.hidden_images

    def game_loop(self, selected_images, hidden_images, rows, cols, num_bombs):
        """Main game loop for playing the level."""
        selection1, selection2 = None, None
        flip_back_time = None
        start_time = pygame.time.get_ticks()
        matched_cards = set()

        game_loop_running = True
        clock = pygame.time.Clock()

        while game_loop_running:
            clock.tick(30)
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for idx, rect in enumerate(self.nem_pics_rect):
                        if hidden_images[idx] or idx in matched_cards:
                            continue
                        if rect.collidepoint(event.pos):
                            if selected_images[idx] == "bomb":
                                # Show bomb and shuffle unmatched cards
                                hidden_images[idx] = True
                            elif selection1 is None:
                                selection1 = idx
                                hidden_images[selection1] = True
                            elif selection2 is None and idx != selection1:
                                selection2 = idx
                                hidden_images[selection2] = True
                                flip_back_time = pygame.time.get_ticks() + 1000

            if flip_back_time and pygame.time.get_ticks() >= flip_back_time:
                if selected_images[selection1] != selected_images[selection2]:
                    hidden_images[selection1] = False
                    hidden_images[selection2] = False
                else:
                    matched_cards.update([selection1, selection2])
                selection1, selection2, flip_back_time = None, None, None

            self.screen.blit(self.bg_image, (0, 0))  # Main game background

            for idx in range(len(selected_images)):
                if hidden_images[idx] or idx in matched_cards:
                    self.screen.blit(self.nem_pics[idx], self.nem_pics_rect[idx])
                else:
                    pygame.draw.rect(self.screen, self.GRAY, self.nem_pics_rect[idx], border_radius=15)

            timer_text = self.font.render(f"Time: {elapsed_time:.2f}s", True, (255, 255, 255))
            self.screen.blit(timer_text, (10, 10))

            if len(matched_cards) == len(selected_images) - num_bombs:
                print("You Win!")
                game_loop_running = False

            pygame.display.update()
