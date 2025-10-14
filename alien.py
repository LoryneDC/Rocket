import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load and scale the alien image
        self.image = pygame.image.load('alien.bmp')
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = 50
        self.rect.y = 50

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def update(self):
        """Move the alien to the right."""
        self.x += self.settings.alien_speed
        self.rect.x = self.x
