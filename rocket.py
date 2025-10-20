import sys
import pygame
from random import randint
from settings_class import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from raindrop import Raindrop  # 🌧 Import the new Raindrop class


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
        self.stars = pygame.sprite.Group()
        self.raindrops = pygame.sprite.Group()  # 🌧 Raindrop group

        # Create all static/background elements
        self._create_star_field()
        self._create_fleet()
        self._create_rain()

    # ---------------- GAME LOOP ---------------- #
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_rain()   # 🌧 Move raindrops
            self._update_screen()

    # ---------------- STAR FIELD ---------------- #
    def _create_star_field(self):
        """Create a grid of stars with random offsets for realism."""
        star = Star(self)
        star_width, star_height = star.rect.size

        available_space_x = self.settings.screen_width - (2 * star_width)
        available_space_y = self.settings.screen_height - (2 * star_height)
        number_stars_x = available_space_x // (2 * star_width)
        number_rows = available_space_y // (2 * star_height)

        for row_number in range(number_rows):
            for star_number in range(number_stars_x):
                self._create_star(star_number, row_number)

    def _create_star(self, star_number, row_number):
        """Create a single star and place it randomly in the grid."""
        star = Star(self)
        star_width, star_height = star.rect.size
        star.x = star_width + 2 * star_width * star_number
        star.y = star_height + 2 * star_height * row_number
        star.rect.x = star.x + randint(-15, 15)
        star.rect.y = star.y + randint(-15, 15)
        self.stars.add(star)

    # ---------------- ALIEN FLEET ---------------- #
    def _update_aliens(self):
        """Update alien fleet positions."""
        self._check_fleet_edges()
        self.aliens.update()

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

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if hasattr(alien, "check_edges") and alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    # ---------------- RAIN SYSTEM ---------------- #
    def _create_rain(self):
        """Create a grid of raindrops across the top of the screen."""
        raindrop = Raindrop(self)
        raindrop_width, raindrop_height = raindrop.rect.size

        available_space_x = self.settings.screen_width - (2 * raindrop_width)
        available_space_y = self.settings.screen_height
        number_raindrops_x = available_space_x // (2 * raindrop_width)
        number_rows = available_space_y // (2 * raindrop_height)

        for row_number in range(number_rows // 2):  # Half the screen for initial rain
            for raindrop_number in range(number_raindrops_x):
                self._create_raindrop(raindrop_number, row_number)

    def _create_raindrop(self, raindrop_number, row_number):
        """Create a single raindrop and place it in the grid."""
        raindrop = Raindrop(self)
        raindrop_width, raindrop_height = raindrop.rect.size
        raindrop.x = raindrop_width + 2 * raindrop_width * raindrop_number
        raindrop.y = raindrop_height + 2 * raindrop_height * row_number
        raindrop.rect.x = raindrop.x + randint(-10, 10)
        raindrop.rect.y = raindrop.y + randint(-10, 10)
        self.raindrops.add(raindrop)

    def _update_rain(self):
        """Move raindrops and recycle new ones when they disappear."""
        self.raindrops.update()

        # Remove raindrops that have fallen off the bottom
        for raindrop in self.raindrops.copy():
            if raindrop.rect.top >= self.settings.screen_height:
                self.raindrops.remove(raindrop)

        # 🌧 Steady rain: add new row at the top
        if len(self.raindrops) == 0 or randint(0, 10) > 8:
            self._create_rain()

    # ---------------- BULLETS ---------------- #
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    # ---------------- EVENTS ---------------- #
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

        # 🌧 Draw raindrops next (falling layer)
        self.raindrops.draw(self.screen)

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
