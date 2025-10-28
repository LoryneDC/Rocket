import sys
from time import sleep

import pygame

from random import randint, random  # For randomness
from settings_class import Settings
from game_stats import GameStats
from button import Button
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

        # Necesario para el posicionamiento central de botones
        self.screen_rect = self.screen.get_rect() 

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

        # Make the Play button.
        self.play_button = Button(self, "Play")

        # Make the Difficulty buttons
        self.easy_button = Button(self, "Easy")
        self.medium_button = Button(self, "Medium")
        self.hard_button = Button(self, "Hard")
        
        # --- Posicionamiento de Botones (Fijos) ---
        
        # Posición central de referencia
        center_y = self.screen_rect.centery 
        y_spacing = self.play_button.rect.height + 20 # Espacio entre botones
        
        # Posicionar Easy, Medium y Hard arriba del centro
        # Easy: -1.5 espacios desde el centro
        self.easy_button.rect.centery = center_y - (1.5 * y_spacing) 
        # Medium: -0.5 espacios desde el centro
        self.medium_button.rect.centery = center_y - (0.5 * y_spacing) 
        # Hard: +0.5 espacios desde el centro
        self.hard_button.rect.centery = center_y + (0.5 * y_spacing)  

        # Posicionar el botón Play (para "Continuar" o "Game Over")
        # Play: +2.5 espacios desde el centro
        self.play_button.rect.centery = center_y + (2.5 * y_spacing)

        # Start with medium difficulty selected (or default)
        self.settings.set_difficulty('medium')

    # ---------------- MAIN GAME LOOP ---------------- #
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
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
        self.stats.ship_hits += 1  # Track how many times ship is hit

        if self.stats.ship_hits >= 3:  # Game over condition
            print("💀 GAME OVER: Ship was hit too many times!")
            self.stats.game_active = False
            return

        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

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

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

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
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            self.stats.alien_hits += 1
            print(f"🚀 Alien hit! Total: {self.stats.alien_hits}")

            if self.stats.alien_hits >= 1000   :  # Example win condition
                print("🏆 YOU WIN! All aliens destroyed!")
                self.stats.game_active = False

        if not self.aliens:
            # Destroy existing bullets and create new
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _start_game(self):
        """A consolidated method to start a new game."""
        # Note: initialize_dynamic_settings() is now done in set_difficulty(), 
        # but calling it here ensures speeds are reset if 'p' is pressed before a button.
        self.settings.initialize_dynamic_settings()

        # Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True

        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        print("🎮 Game started!") # Add feedback for keyboard start

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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play or selects difficulty."""
        if not self.stats.game_active:
            # ... (código para play_button_clicked)

            # Check for Difficulty buttons (Inactive state)
            easy_clicked = self.easy_button.rect.collidepoint(mouse_pos)
            medium_clicked = self.medium_button.rect.collidepoint(mouse_pos)
            hard_clicked = self.hard_button.rect.collidepoint(mouse_pos)

            if easy_clicked:
                self.settings.set_difficulty('easy')
                self._start_game() # <-- Inicia el juego
            elif medium_clicked:
                self.settings.set_difficulty('medium')
                self._start_game() # <-- Inicia el juego
            elif hard_clicked:
                self.settings.set_difficulty('hard')
                self._start_game() # <-- Inicia el juego
            
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
        # New: Start game with 'p' key
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()

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

        font = pygame.font.SysFont(None, 36)
        hits_text = font.render(f"Ship hits: {self.stats.ship_hits} | Alien hits: {self.stats.alien_hits}", True, (255, 255, 255))
        self.screen.blit(hits_text, (20, 20))

        # Draw the buttons if the game is inactive.
        if not self.stats.game_active:
            # Draw the buttons below the score text
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()
            
            # Optional: Add a note to press 'P'
            font = pygame.font.SysFont(None, 36)
            press_p_text = font.render("Press P to Play", True, (255, 255, 255))
            p_text_rect = press_p_text.get_rect(center=(self.settings.screen_width // 2, self.hard_button.rect.bottom + 50))
            self.screen.blit(press_p_text, p_text_rect)

        pygame.display.flip()


# ---------------- MAIN EXECUTION ---------------- #
if __name__ == "__main__":
    ai = Rocket()
    ai.run_game()