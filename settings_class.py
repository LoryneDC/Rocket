class Settings:
    """A class to store all settings for Rocket."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (30, 15, 46)
        #self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (232, 178, 77)
        self.bullets_allowed = 3
        
        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settins that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Inside Settings.__init__
        self.raindrop_speed = 1.2 

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

    def set_difficulty(self, level='medium'):
        """Set game parameters based on the chosen difficulty level."""
        self.initialize_dynamic_settings() # Start from base speeds

        if level == 'easy':
            self.ship_limit = 5          # More lives
            self.alien_speed *= 0.8      # Slower aliens
            self.bullets_allowed = 5     # More bullets
            self.fleet_drop_speed = 5    # Slower drop
        elif level == 'hard':
            self.ship_limit = 2          # Fewer lives
            self.alien_speed *= 1.5      # Faster aliens
            self.bullets_allowed = 2     # Fewer bullets
            self.fleet_drop_speed = 20   # Faster drop
        else: # Medium (Default)
            # Default settings already set up for medium
            pass
        

