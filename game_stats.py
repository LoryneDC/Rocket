class GameStats:
    """Track statistics for Alien Invasion (Rocket.py)."""

    def __init__(self, ai_game):
        """Initialize statistics."""

        self.settings = ai_game.settings
        self.reset_stats()

        # Start Alien Invasion (Rocket) in an active state.
        self.game_active = True

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
