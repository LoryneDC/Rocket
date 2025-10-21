class Settings:
    """A class to store all settings for Rocket."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (30, 15, 46)
        #self.bg_color = (230, 230, 230)

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (232, 56, 228)
        self.bullets_allowed = 3
        
        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents risght: -1 represents left.
        self.fleet_direction = 1

        # Inside Settings.__init__
        self.raindrop_speed = 1.2  # lower = slower, higher = faster
