import pygame
from UI.main_menu import main_menu
from modules.game_configuration import MemoryCardGame
from modules.timer_countdown import TimerCountdown

# Initialize Pygame
pygame.init()

# Initialize Game Configuration
game = MemoryCardGame()

# Fonts
def get_font(size):
    return pygame.font.Font("UI/Pixelicious.ttf", size)

# Start game function
def start_game():
    print("Starting game...")  # Replace with your game logic

# Main function
def main():
    screen = pygame.display.set_mode((1280, 720))  # Set screen size
    pygame.display.set_caption("Memory Card Game")
    main_menu(screen, start_game, get_font)  # Call the main menu

if __name__ == "__main__":
    main()
