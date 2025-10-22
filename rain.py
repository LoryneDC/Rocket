# rain.py
import pygame
from pygame.sprite import Sprite


class Raindrop(Sprite):
    """A class to represent a single raindrop."""

    def __init__(self, ai_game):
        """Initialize the raindrop and set its position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load and scale the raindrop image
        self.image = pygame.image.load('/home/krobus/Documents/rocket_project/assets/images/puntoluz.png')
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()

        # Start each new drop near the top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the raindrop’s exact position
        self.y = float(self.rect.y)

    def update(self):
        """Move the raindrop down the screen."""
        self.y += self.settings.raindrop_speed
        self.rect.y = self.y
