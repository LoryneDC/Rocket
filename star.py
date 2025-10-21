import pygame
from pygame.sprite import Sprite

class Star(Sprite):
    """A class to represent a single star."""

    def __init__(self, ai_game):
        """Initialize the star and set its position."""
        super().__init__()
        self.screen = ai_game.screen

        # Load and scale the star image
        self.image = pygame.image.load('/home/krobus/Documents/rocket_project/assets/images/point.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()

        # Start each new star near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the star's exact position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
