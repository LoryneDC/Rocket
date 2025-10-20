# raindrop.py
import pygame
from pygame.sprite import Sprite

class Raindrop(Sprite):
    """A class to represent a single raindrop."""

    def __init__(self, ai_game):
        """Initialize the raindrop and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen

        # Load and scale the raindrop image
        self.image = pygame.image.load('raindrop.png')
        self.image = pygame.transform.scale(self.image, (30, 50))
        self.rect = self.image.get_rect()

        # Start each new raindrop near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the raindrop’s exact vertical position
        self.y = float(self.rect.y)

        # Movement speed (you can tweak this for faster rain)
        self.speed = 1.5

    def update(self):
        """Move the raindrop downward."""
        self.y += self.speed
        self.rect.y = self.y
