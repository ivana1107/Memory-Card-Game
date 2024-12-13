import pygame
import random
import os
from UI_app.end_screens import end_screen

class MemoryCardGame:
    def __init__(self, game_width=1200, game_height=760, pic_size=128, padding=10, left_margin=75, top_margin=70):
        pygame.init()

        # Game configuration
        self.font = pygame.font.Font("UI_app/Pixelicious.ttf", 30)
        self.game_width = game_width
        self.game_height = game_height
        self.pic_size = pic_size
        self.padding = padding
        self.left_margin = left_margin
        self.top_margin = top_margin

        # Colors
        self.WHITE, self.BLACK, self.GRAY = (255, 255, 255), (0, 0, 0), (200, 200, 200)

        # Screen setup
        self.screen = pygame.display.set_mode((self.game_width, self.game_height))
        pygame.display.set_caption("Memory Card Game")

        # Load assets
        self.load_assets()

    def load_assets(self):
        """Load all required images and assets."""
        game_icon = pygame.image.load('UI_app/game_layout.png')
        pygame.display.set_icon(game_icon)

        # Background images
        self.bg_image = pygame.image.load('UI_app/game_layout.png')
        self.bg_image = pygame.transform.scale(self.bg_image, (self.game_width, self.game_height))

        # Bomb image
        self.bomb_image = pygame.image.load(os.path.join('images', 'bomb.png'))
        self.bomb_image = pygame.transform.scale(self.bomb_image, (self.pic_size, self.pic_size))

        # Load memory pictures
        try:
            self.memory_pictures = [os.path.splitext(file)[0] for file in os.listdir('images') if file.endswith(('.png', '.jpg', '.jpeg'))]
            self.memory_pictures = self.memory_pictures[:13]  # Limit to 13 pairs for consistency
        except FileNotFoundError as e:
            print(f"Error loading memory pictures: {e}")

    def get_font(self, size):
        return pygame.font.Font("UI_app/Pixelicious.ttf", size)

    def run(self, level=None):
        """Main game loop with support for difficulty levels."""
        if level is None:
            print("No difficulty level selected, exiting.")
            return

        print(f"Starting game at {level} difficulty.")

        # Create a Level instance to manage the level-specific setup and loop
        level_manager = Level(self.screen, self.bg_image, self.game_width, self.game_height, self.get_font(30), self.GRAY)

        # Set up the game with the selected difficulty
        try:
            nem_pics, nem_pics_rect, selected_images, hidden_images = level_manager.setup_game(level)
        except ValueError as e:
            print(f"Error setting up the game: {e}")
            pygame.quit()
            return

        # Start the game loop for the selected level
        level_manager.game_loop(selected_images, hidden_images)

        print("Game over!")



class Level:
    def __init__(self, screen, bg_image, game_width, game_height, font, gray_color):
        self.screen = screen
        self.bg_image = bg_image
        self.game_width = game_width
        self.game_height = game_height
        self.font = font
        self.GRAY = gray_color

    def setup_game(self, level):
        """Configure game setup based on difficulty level."""
        self.memory_pictures = [item.split('.')[0] for item in os.listdir('images') if item.endswith(('.png', '.jpg', '.jpeg'))]

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

        # Reset variables for the game
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

        # Set the position of each image
        for i in range(len(self.nem_pics_rect)):
            self.nem_pics_rect[i][0] = self.left_margin + ((self.pic_size + self.padding) * (i % self.cols))
            self.nem_pics_rect[i][1] = self.top_margin + ((self.pic_size + self.padding) * (i // self.cols))
            self.hidden_images.append(True)

        return self.nem_pics, self.nem_pics_rect, selected_images, self.hidden_images

    def game_loop(self, selected_images, hidden_images):
        """Main game loop."""
        matched_cards = set()
        clock = pygame.time.Clock()

        while True:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for idx, rect in enumerate(self.nem_pics_rect):
                        if hidden_images[idx] or idx in matched_cards:
                            continue
                        if rect.collidepoint(event.pos):
                            self.flip_card(idx, selected_images, hidden_images, matched_cards)

            # Check if all pairs are matched (except bombs)
            if len(matched_cards) == len(selected_images) - self.num_bombs:
                print("You Win!")
                end_screen(self.screen, "win", self.restart_game, self.main_menu, self.font)
                return

            pygame.display.update()

    def flip_card(self, idx, selected_images, hidden_images, matched_cards):
        """Flip the selected card and check for matches."""
        # Implement card flipping and match checking logic
        pass

    def restart_game(self):
        """Restart the game."""
        self.game.run("easy")  # or any default level

    def main_menu(self):
        """Go back to the main menu."""
        self.game.run()  # Go back to the main menu setup
