class Jugador:
    def __init__(self, color, name=None):
        """Initialize a player."""
        self.color = color
        self.color_names = ['Rojo', 'Azul', 'Verde', 'Amarillo']
        self.name = name if name else self.color_names[color]
        self.consecutive_pairs = 0  # Track consecutive pair counts
        self.last_moved_piece = None  # Track last moved piece

    def get_color(self):
        """Get player's color."""
        return self.color

    def get_name(self):
        """Get player's name."""
        return self.name

    def set_name(self, name):
        """Set player's name."""
        self.name = name

    def add_consecutive_pair(self):
        """Increment the count of consecutive pairs."""
        self.consecutive_pairs += 1
        return self.consecutive_pairs

    def reset_consecutive_pairs(self):
        """Reset the count of consecutive pairs."""
        self.consecutive_pairs = 0

    def set_last_moved_piece(self, piece_id):
        """Set the ID of the last moved piece."""
        self.last_moved_piece = piece_id
        return piece_id

    def get_last_moved_piece(self):
        """Get the ID of the last moved piece."""
        return self.last_moved_piece


class GestorJugadores:
    def __init__(self, num_players=4):
        """Initialize the player manager."""
        self.num_players = min(max(num_players, 2), 4)  # Between 2 and 4 players
        self.players = self._create_players()
        self.current_player_index = 0

    def _create_players(self):
        """Create all players for the game."""
        return [Jugador(i) for i in range(self.num_players)]

    def get_current_player(self):
        """Get the current player."""
        return self.players[self.current_player_index]

    def next_player(self):
        """Move to the next player."""
        self.current_player_index = (self.current_player_index + 1) % self.num_players
        return self.get_current_player()

    def get_player(self, index):
        """Get a specific player by index."""
        return self.players[index % self.num_players]

    def get_player_by_color(self, color):
        """Get a player by color."""
        for player in self.players:
            if player.get_color() == color:
                return player
        return None

    def set_player_name(self, index, name):
        """Set a player's name."""
        self.players[index % self.num_players].set_name(name)