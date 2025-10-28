import pygame.font

class Button:
    """A class to create and draw buttons."""

    def __init__(self, ai_game, msg):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set dimensions and properties
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)  # Green
        self.text_color = (255, 255, 255)  # White
        self.font = pygame.font.SysFont(None, 48)

        # Build the button’s rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Prepare the button message
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and save it."""
        # Solo renderiza la imagen.
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        # Nota: El centrado final se hace en draw_button.

    def draw_button(self):
        """Draw blank button and then draw message."""
        # CORRECCIÓN: Centra la imagen del texto DENTRO del rectángulo del botón
        # justo antes de dibujar. Esto asegura que si movemos self.rect, el texto lo siga.
        self.msg_image_rect.center = self.rect.center
        
        # Dibuja el rectángulo del botón.
        self.screen.fill(self.button_color, self.rect)
        
        # Dibuja la imagen del texto.
        self.screen.blit(self.msg_image, self.msg_image_rect)