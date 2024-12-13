import pygame

class Flip:
    def __init__(self, game, image, rect, is_bomb=False):
        self.game = game
        self.image = image
        self.rect = rect
        self.is_bomb = is_bomb
        self.hidden = True
        self.flipping = False
        self.flip_progress = 0  # 0 to 1, indicates the animation state

    def draw(self, screen):
        if self.flipping:
            # Animate flipping effect by scaling image or rectangle
            flip_width = int(self.rect.width * (1 - abs(1 - 2 * self.flip_progress)))
            if flip_width > 0:
                scaled_image = pygame.transform.scale(self.image, (flip_width, self.rect.height))
                scaled_rect = scaled_image.get_rect(center=self.rect.center)
                screen.blit(scaled_image, scaled_rect)
            else:
                # Show the back of the card when fully "flipped"
                pygame.draw.rect(screen, self.game.GRAY, self.rect, border_radius=15)
        elif not self.hidden:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, self.game.GRAY, self.rect, border_radius=15)
    
    def update(self, delta_time):
        if self.flipping:
            self.flip_progress += delta_time * 2  # Adjust speed as needed
            if self.flip_progress >= 1:
                self.flipping = False
                self.flip_progress = 0
                if not self.is_bomb:
                    self.hidden = not self.hidden  # Toggle hidden state when animation ends

    def start_flip(self):
        if not self.flipping:
            self.flipping = True
            self.flip_progress = 0

