import pygame
import sys
import random
from modules.game_configuration import MemoryCardGame
from modules.timer_countdown import TimerCountdown  
from UI_app.main_menu import main_menu  # Import the menu display function
from UI_app.end_screens import end_screen  # Import the end screen functionality

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# Load Background Music
pygame.mixer.music.load('star.mp3')
pygame.mixer.music.play(-1)  # Play music in a loop

# Initialize Game Configuration
game = MemoryCardGame()

# Main loop
if __name__ == "__main__":
    # Display the main menu and get the selected difficulty level
    selected_level = main_menu(game.screen, game.run, game.get_font)  # Fetch selected level, passing game.get_font
    
    # Setup the game board based on the selected difficulty
    game.setup_game(selected_level)  # Initialize the game with the selected level
    
    # Start the game loop for the selected level
    game.game_loop()  # Start the game loop with the configured level
