# game.py
import pygame
from modules.game_configuration import game_loop
from UI_app.main_menu import main_menu
from modules.game_configuration import MemoryCardGame

def start_game():
    # Initialize Pygame and create a game instance
    pygame.init()
    game = MemoryCardGame()

    # Display the main menu and get the selected level
    selected_level = main_menu(game.screen, game.run, game.get_font)

    # Start the game loop with the selected difficulty level
    game_loop(selected_level)

if __name__ == "__main__":
    start_game()
