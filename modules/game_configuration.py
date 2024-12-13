import pygame
import os

class MemoryCardGame:
    def __init__(self, game_width=1200, game_height=760, pic_size=128, padding=10, left_margin=75, top_margin=70):
        # Initialize Pygame
        pygame.init()
        
        # Game configuration
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
        pygame.display.set_caption("Flip and Find")
        
        # Fonts
        self.font = pygame.font.Font(None, 74)
        self.button_font = pygame.font.Font(None, 50)
        
        # Images
        self.bg_image = None
        self.congrats_bg_image = None
        self.bomb_image = None
        self.cards = []
        self.memory_pictures = []
        self.nem_pics = []
        self.nem_pics_rect = []
        self.hidden_images = []

        # Load assets
        self.load_assets()

    def load_assets(self):
        """Load all required images and assets."""
        # Game icon
        game_icon = pygame.image.load('backg.png')
        pygame.display.set_icon(game_icon)
        
        # Background images
        self.bg_image = pygame.image.load('backg.png')
        self.bg_image = pygame.transform.scale(self.bg_image, (self.game_width, self.game_height))
        
        self.congrats_bg_image = pygame.image.load('backg.png')
        self.congrats_bg_image = pygame.transform.scale(self.congrats_bg_image, (self.game_width, self.game_height))
        
        # Bomb image
        self.bomb_image = pygame.image.load(os.path.join('images', 'bomb.png'))
        self.bomb_image = pygame.transform.scale(self.bomb_image, (self.pic_size, self.pic_size))
        
        # Load memory pictures
        try:
            self.memory_pictures = [os.path.splitext(file)[0] for file in os.listdir('images') if file.endswith(('.png', '.jpg', '.jpeg'))]
            self.memory_pictures = self.memory_pictures[:13]  # Limit to 13 pairs for consistency
        except FileNotFoundError as e:
            print(f"Error loading memory pictures: {e}")
        
    def draw_background(self):
        """Draw the background image."""
        self.screen.blit(self.bg_image, (0, 0))

    def run(self):
        """Main game loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.draw_background()
            pygame.display.flip()
        
        pygame.quit()

# Initialize and run the game
if __name__ == "__main__":
    game = MemoryCardGame()
    game.run()
