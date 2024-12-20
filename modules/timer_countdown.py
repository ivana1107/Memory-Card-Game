import pygame
import sys

class TimerCountdown:
    def __init__(self, screen, font, level):
        self.screen = screen
        self.font = font
        self.level = level
        self.time_limits = {"easy": 30, "medium": 50, "hard": 80}
        self.start_time = pygame.time.get_ticks()
        self.time_limit = self.time_limits[level]
        self.time_left = self.time_limit

    def update(self):
        # Calculate time left
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        self.time_left = max(0, self.time_limit - elapsed_time)

    def display(self):
        # Render and display the timer on the top right
        timer_text = self.font.render(f"Time: {int(self.time_left)}s", True, (255, 255, 255))
        timer_x = self.screen.get_width() - timer_text.get_width() - 20
        self.screen.blit(timer_text, (timer_x, 10))

    def is_time_up(self):
        # Check if time is up
        return self.time_left <= 0