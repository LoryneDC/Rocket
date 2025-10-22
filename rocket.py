import sys
from time import sleep

import pygame

from random import randint, random  # For randomness
from settings_class import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from rain import Raindrop  # Import the new Raindrop class


class Rocket:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Rocket")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.raindrops = pygame.sprite.Group()  # 🌧️ Group for raindrops

        # Create background elements
        self._create_star_field()
        self._create_rain_field()
        self._create_fleet()

    # ---------------- MAIN GAME LOOP ---------------- #
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_raindrops()  # 🌧️ Update rain
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
                if random() < 0.3:  # 30% chance to spawn each star
                    self._create_star(star_number, row_number)

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""

        # Decrement ships_left.
        self.stats.ships_left -= 1

        # Get rid of any reaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        # Pause.
        sleep(0.5)

    def _create_star(self, star_number, row_number):
        """Create a single star and place it randomly in the grid."""
        star = Star(self)
        star_width, star_height = star.rect.size
        star.x = star_width + 2 * star_width * star_number
        star.y = star_height + 2 * star_height * row_number

        # Random offset for more natural look
        star.rect.x = star.x + randint(-15, 15)
        star.rect.y = star.y + randint(-15, 15)
        self.stars.add(star)

    # ---------------- RAIN FIELD ---------------- #
    def _create_rain_field(self):
        """Create an initial grid of raindrops with randomness."""
        raindrop = Raindrop(self)
        drop_width, drop_height = raindrop.rect.size
        available_space_x = self.settings.screen_width - (2 * drop_width)
        available_space_y = self.settings.screen_height - (2 * drop_height)
        number_drops_x = available_space_x // (2 * drop_width)
        number_rows = available_space_y // (2 * drop_height)

        for row_number in range(number_rows):
            for drop_number in range(number_drops_x):
                # Only spawn some of the drops for realism
                if random() < 0.25:  # 25% chance to spawn each drop
                    self._create_raindrop(drop_number, row_number)

    def _create_raindrop(self, drop_number, row_number):
        """Create a single raindrop and place it in the grid."""
        raindrop = Raindrop(self)
        drop_width, drop_height = raindrop.rect.size
        raindrop.x = drop_width + 2 * drop_width * drop_number
        raindrop.rect.x = raindrop.x + randint(-10, 10)
        raindrop.rect.y = raindrop.rect.height + 2 * raindrop.rect.height * row_number
        self.raindrops.add(raindrop)

    def _update_raindrops(self):
        """Make the raindrops fall steadily and respawn from the top."""
        self.raindrops.update()
        screen_rect = self.screen.get_rect()

        # Remove drops that fall below the screen
        for drop in self.raindrops.copy():
            if drop.rect.top >= screen_rect.bottom:
                self.raindrops.remove(drop)

        # Occasionally create new raindrops at the top
        if randint(0, 12) == 0:  # Higher number = less frequent rain
            self._create_raindrop(randint(0, 20), 0)

    # ---------------- ALIEN FLEET ---------------- #
    def _update_aliens(self):
        """Check fleet edges and update alien positions."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (
            self.settings.screen_height - (3 * alien_height) - ship_height
        )
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change its direction."""
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

    # ---------------- BULLETS ---------------- #
    def _update_bullets(self):
        """Update bullet positions and remove off-screen bullets."""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.

        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()

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
        """Update images on the screen and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)

        # Draw background elements first
        self.stars.draw(self.screen)
        self.raindrops.draw(self.screen)

        # Then draw gameplay elements
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        pygame.display.flip()


# ---------------- MAIN EXECUTION ---------------- #
if __name__ == "__main__":
    ai = Rocket()
    ai.run_game()
