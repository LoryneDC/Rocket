import sys
import pygame
from random import randint  # For random star placement
from settings_class import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star  # Import your Star class


class Rocket:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Rocket")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()  # ⭐ Group for stars

        # Create the background stars and alien fleet
        self._create_star_field()
        self._create_fleet()

    # ---------------- GAME LOOP ---------------- #
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()

    # ---------------- STAR FIELD ---------------- #
    def _create_star_field(self):
        """Create a grid of stars with random offsets for realism."""
        star = Star(self)
        star_width, star_height = star.rect.size

        # Determine how many stars fit horizontally and vertically
        available_space_x = self.settings.screen_width - (2 * star_width)
        available_space_y = self.settings.screen_height - (2 * star_height)
        number_stars_x = available_space_x // (2 * star_width)
        number_rows = available_space_y // (2 * star_height)

        # Create grid with randomness
        for row_number in range(number_rows):
            for star_number in range(number_stars_x):
                self._create_star(star_number, row_number)

    def _create_star(self, star_number, row_number):
        """Create a single star and place it randomly in the grid."""
        star = Star(self)
        star_width, star_height = star.rect.size

        # Regular grid placement
        star.x = star_width + 2 * star_width * star_number
        star.y = star_height + 2 * star_height * row_number

        # Random offset for more natural distribution
        star.rect.x = star.x + randint(-15, 15)
        star.rect.y = star.y + randint(-15, 15)

        self.stars.add(star)

    # ---------------- ALIEN FLEET ---------------- #
    def _create_fleet(self):
        """Create the fleet of aliens."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    # ---------------- BULLETS ---------------- #
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    # ---------------- EVENT HANDLING ---------------- #
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    # ---------------- FIRING ---------------- #
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    # ---------------- SCREEN UPDATE ---------------- #
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)

        # Draw the stars first (background)
        self.stars.draw(self.screen)

        # Then draw other game elements
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        pygame.display.flip()


# ---------------- MAIN EXECUTION ---------------- #
if __name__ == '__main__':
    ai = Rocket()
    ai.run_game()
