import pygame
import os
import random
import sys
from modules.game_configuration import MemoryCardGame
from modules.timer_countdown import TimerCountdown
from modules.shuffle_bomb import Shuffle

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# Load Background Music
pygame.mixer.music.load('star.mp3')
pygame.mixer.music.play(-1)  # Play music in a loop

# Initialize Game Configuration
game = MemoryCardGame()

def setup_game(level):
    # Define grid and bomb configuration
    rows, cols, num_bombs = {
        "easy": (3, 3, 1),    # 3x3 grid with 1 bomb
        "medium": (4, 4, 2),  # 4x4 grid with 2 bombs
        "hard": (5, 5, 3),    # 5x5 grid with 3 bombs
    }[level]

    num_pairs = (rows * cols - num_bombs) // 2

    # Ensure there are enough unique images for the selected level
    if num_pairs > len(game.memory_pictures):
        raise ValueError("Not enough unique images for the selected level.")

    # Dynamic card size and padding calculation
    grid_width = game.game_width - 2 * game.left_margin
    grid_height = game.game_height - 2 * game.top_margin
    game.pic_size = min(grid_width // cols, grid_height // rows) - 10  # Adjust with padding
    game.padding = 10
    game.left_margin = (game.game_width - (game.pic_size + game.padding) * cols + game.padding) // 2
    game.top_margin = (game.game_height - (game.pic_size + game.padding) * rows + game.padding) // 2

    # Select images for the game
    selected_images = random.sample(game.memory_pictures, num_pairs)
    selected_images *= 2  # Duplicate to make pairs
    selected_images += ["bomb"] * num_bombs
    random.shuffle(selected_images)

    # Reset global variables
    game.nem_pics.clear()
    game.nem_pics_rect.clear()
    game.hidden_images.clear()

    # Load images and set positions
    for item in selected_images:
        picture = pygame.image.load(f'images/{item}.png')
        picture = pygame.transform.scale(picture, (game.pic_size, game.pic_size))
        game.nem_pics.append(picture)
        pictureRect = picture.get_rect()
        game.nem_pics_rect.append(pictureRect)

    for i, rect in enumerate (game.nem_pics_rect):
        rect.x = game.left_margin + ((game.pic_size + game.padding) * (i % cols))
        rect.y = game.top_margin + ((game.pic_size + game.padding) * (i // cols))
        game.hidden_images.append(False)

    return rows, cols, num_bombs, selected_images


###def display_menu():
    menu_running = True
    while menu_running:
        game.draw_background()
        title_text = game.font.render("Memory Card Game", True, game.WHITE)
        game.screen.blit(title_text, (game.game_width // 2 - title_text.get_width() // 2, 100))

        button_texts = ["Easy", "Medium", "Hard", "Exit"]
        buttons = []

        for i, text in enumerate(button_texts):
            button_rect = pygame.Rect(
                game.game_width // 2 - 100, 200 + i * 100, 200, 80
            )
            buttons.append(button_rect)
            pygame.draw.rect(game.screen, game.GRAY, button_rect)
            text_render = game.button_font.render(text, True, game.BLACK)
            game.screen.blit(
                text_render,
                (
                    button_rect.x + (button_rect.width - text_render.get_width()) // 2,
                    button_rect.y + (button_rect.height - text_render.get_height()) // 2,
                ),
            )

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(buttons):
                    if rect.collidepoint(event.pos):
                        if button_texts[i] == "Exit":
                            pygame.quit()
                            exit()
                        return button_texts[i].lower()


def game_loop(level):
    rows, cols, num_bombs, memory_pictures = setup_game(level)
    selection1, selection2 = None, None
    flip_back_time = None
    matched_cards = set()

    clock = pygame.time.Clock()
    timer = TimerCountdown(game.screen, game.font, level)

    shuffle_bomb = Shuffle(
        memory_pictures,
        game.hidden_images,
        game.nem_pics,
        game.nem_pics_rect,
        rows,
        cols,
        game.left_margin,
        game.top_margin,
        game.pic_size,
        game.padding,
    )
    
    while True:
        clock.tick(30)
        timer.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for idx, rect in enumerate(game.nem_pics_rect):
                    if game.hidden_images[idx] or idx in matched_cards:
                        continue
                    if rect.collidepoint(event.pos):
                        if memory_pictures[idx] == "bomb":
                            # Show bomb and shuffle unmatched cards
                            game.hidden_images[idx] = True
                            #shuffle_unmatched_cards(memoryPictures, hiddenImages, nemPics, nemPicsRect, rows, cols)
                        elif selection1 is None:
                            selection1 = idx
                            game.hidden_images[selection1] = True
                        elif selection2 is None and idx != selection1:
                            selection2 = idx
                            game.hidden_images[selection2] = True
                            flip_back_time = pygame.time.get_ticks() + 1000

        if flip_back_time and pygame.time.get_ticks() >= flip_back_time:
            if memory_pictures[selection1] != memory_pictures[selection2]:
                game.hidden_images[selection1] = False
                game.hidden_images[selection2] = False
            else:
                matched_cards.update([selection1, selection2])
            selection1, selection2, flip_back_time = None, None, None

        game.draw_background() # Main game background

        for idx, rect in enumerate(game.nem_pics_rect):
            if game.hidden_images[idx] or idx in matched_cards:
                game.screen.blit(game.nem_pics[idx], game.nem_pics_rect[idx])
            else:
                pygame.draw.rect(game.screen, game.GRAY, rect, border_radius=15)
        
        timer.display()

        if len(matched_cards) == len(memory_pictures) - num_bombs:
            # Display the win screen with background
            win_text = game.font.render("Congratulations!", True, game.BLACK)
            game.screen.blit(win_text, (game.game_width // 2 - win_text.get_width() // 2, game.game_height // 2 - 50))
            pygame.display.update()
            pygame.time.wait(3000)
            break

        if timer.is_time_up():
            lose_text = game.font.render("Time's Up! You Lose!", True, game.WHITE)
            game.screen.blit(lose_text, (game.game_width // 2 - lose_text.get_width() // 2, game.game_height // 2 - 50))
            pygame.display.update()
            pygame.time.wait(3000)
            break

        pygame.display.update()


while True:
    selected_level = display_menu()
    game_loop(selected_level)