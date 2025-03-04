class Ficha:
    def __init__(self, color, id_ficha):
        """Initialize a new piece."""
        self.color = color  # Color of the piece (0: Red, 1: Blue, 2: Green, 3: Yellow)
        self.id = id_ficha  # Identifier for the piece (0-3)
        self.position = 0  # 0 means in jail
        self.in_goal = False  # Whether the piece has reached the goal
        self.in_jail = True  # Whether the piece is in jail
        self.in_final_path = False  # Whether the piece is in its final path to goal

    def move(self, steps):
        """Move the piece a given number of steps."""
        if self.in_jail:
            return False

        if self.in_goal:
            return False

        # Update position
        self.position += steps

        # Check if piece reached goal
        return True

    def get_position(self):
        """Get the current position of the piece."""
        return self.position

    def set_position(self, position):
        """Set the position of the piece explicitly."""
        self.position = position
        self.in_jail = (position == 0)
        return True

    def send_to_jail(self):
        """Send the piece back to jail."""
        self.position = 0
        self.in_jail = True
        self.in_final_path = False
        return True

    def reach_goal(self):
        """Mark the piece as having reached the goal."""
        self.in_goal = True
        self.in_jail = False
        self.in_final_path = False
        return True

    def enter_final_path(self):
        """Mark the piece as having entered its final path."""
        self.in_final_path = True
        return True

    def is_in_jail(self):
        """Check if the piece is in jail."""
        return self.in_jail

    def is_in_goal(self):
        """Check if the piece has reached the goal."""
        return self.in_goal

    def is_in_final_path(self):
        """Check if the piece is in its final path."""
        return self.in_final_path


class GestorFichas:
    def __init__(self, num_players=4):
        """Initialize the piece manager."""
        self.num_players = num_players
        self.pieces = self._create_pieces()

        # Define start positions for each color
        self.start_positions = {
            0: 5,  # Red starts at position 5
            1: 22,  # Blue starts at position 22
            2: 39,  # Green starts at position 39
            3: 56  # Yellow starts at position 56
        }

        # Safe positions (general safe spots)
        self.safe_positions = [5, 12, 22, 29, 39, 46, 56, 63]

        # Define entry points to the final paths
        self.final_path_entries = {
            0: 68,  # Red enters final path after position 68
            1: 17,  # Blue enters final path after position 17
            2: 34,  # Green enters final path after position 34
            3: 51  # Yellow enters final path after position 51
        }

        # Goal positions for each color
        self.goal_positions = {
            0: 76,  # Red's goal
            1: 84,  # Blue's goal
            2: 92,  # Green's goal
            3: 100  # Yellow's goal
        }

    def _create_pieces(self):
        """Create all pieces for the game."""
        pieces = {}
        for color in range(self.num_players):
            pieces[color] = []
            for i in range(4):  # 4 pieces per player
                pieces[color].append(Ficha(color, i))
        return pieces

    def get_piece(self, color, piece_id):
        """Get a specific piece."""
        return self.pieces[color][piece_id]

    def get_pieces_for_player(self, color):
        """Get all pieces for a specific player."""
        return self.pieces[color]

    def release_piece(self, color, piece_id):
        """Release a piece from jail to its start position."""
        piece = self.pieces[color][piece_id]
        if piece.is_in_jail():
            start_pos = self.start_positions[color]
            piece.set_position(start_pos)
            piece.in_jail = False
            return True
        return False

    def move_piece(self, color, piece_id, steps):
        """Move a piece a given number of steps considering the rules."""
        piece = self.pieces[color][piece_id]
        current_pos = piece.get_position()

        # If in jail, can't move
        if piece.is_in_jail():
            return False

        # If already in goal, can't move
        if piece.is_in_goal():
            return False

        # Check if we're in final path or need to enter it
        if piece.is_in_final_path():
            new_pos = current_pos + steps

            # If exceeds goal, can't move
            if new_pos > self.goal_positions[color]:
                return False

            # If reaches goal exactly
            if new_pos == self.goal_positions[color]:
                piece.reach_goal()
                return True

            # Otherwise, just move in the final path
            piece.set_position(new_pos)
            return True
        else:
            # Check if we need to enter final path
            entry_pos = self.final_path_entries[color]

            # Calculate the external path position (wrapping around 1-68)
            new_pos = ((current_pos - 1 + steps) % 68) + 1

            # Check if we cross or land on the entry point
            if current_pos <= entry_pos and (current_pos + steps) > entry_pos:
                # Calculate how many steps we took after the entry point
                steps_after_entry = (current_pos + steps) - entry_pos

                # Enter the final path
                piece.enter_final_path()

                # Set position to the first position in final path + remaining steps
                final_path_start = self.goal_positions[color] - 7  # 8 positions in final path
                piece.set_position(final_path_start + steps_after_entry - 1)

                # Check if we reached the goal exactly
                if piece.get_position() == self.goal_positions[color]:
                    piece.reach_goal()

                return True
            else:
                # Standard move on the external path
                piece.set_position(new_pos)
                return True

    def get_position_counts(self):
        """Get a dictionary with counts of pieces at each position."""
        position_counts = {}

        for color in range(self.num_players):
            for piece in self.pieces[color]:
                pos = piece.get_position()
                if pos not in position_counts:
                    position_counts[pos] = []
                position_counts[pos].append((color, piece.id))

        return position_counts

    def is_blockade(self, position):
        """Check if there's a blockade at the given position."""
        position_counts = self.get_position_counts()

        if position in position_counts:
            pieces_at_pos = position_counts[position]

            # If there are at least 2 pieces at this position
            if len(pieces_at_pos) >= 2:
                # Check if they are from the same color (blockade)
                if pieces_at_pos[0][0] == pieces_at_pos[1][0]:
                    return True

                # Check if they are at a safe position (also blockade)
                if position in self.safe_positions or position in self.start_positions.values():
                    return True

        return False

    def capture_piece(self, position, attacking_color):
        """Capture a piece at the given position."""
        position_counts = self.get_position_counts()

        if position in position_counts:
            for color, piece_id in position_counts[position]:
                # Don't capture pieces of the same color
                if color != attacking_color:
                    # Send the piece back to jail
                    self.pieces[color][piece_id].send_to_jail()
                    return color, piece_id

        return None, None

    def count_pieces_in_goal(self, color):
        """Count how many pieces of a given color have reached the goal."""
        count = 0
        for piece in self.pieces[color]:
            if piece.is_in_goal():
                count += 1
        return count

    def all_pieces_in_goal(self, color):
        """Check if all pieces of a given color have reached the goal."""
        for piece in self.pieces[color]:
            if not piece.is_in_goal():
                return False
        return True

    def check_start_position_capture(self, color):
        """Check if there's a piece of a different color in this color's start position."""
        position_counts = self.get_position_counts()
        start_pos = self.start_positions[color]

        if start_pos in position_counts:
            pieces_at_pos = position_counts[start_pos]

            # Check all pieces at this start position
            for piece_color, piece_id in pieces_at_pos:
                # If it's a piece of a different color, capture it
                if piece_color != color:
                    self.pieces[piece_color][piece_id].send_to_jail()
                    return piece_color, piece_id

        return None, None

    def get_movable_pieces(self, color, dice_values):
        """Get all pieces that can move with the given dice values."""
        movable_pieces = []

        # Check if there are pieces in jail and if we have a 5 to release them
        jail_pieces = [piece.id for piece in self.pieces[color] if piece.is_in_jail()]
        can_release = 5 in dice_values or sum(dice_values) == 5

        # If we can release pieces from jail and there are pieces in jail, it's mandatory
        if can_release and jail_pieces:
            return [(-1, piece_id) for piece_id in jail_pieces]  # -1 indicates "release action"

        # Check all pieces out of jail
        for piece in self.pieces[color]:
            if not piece.is_in_jail() and not piece.is_in_goal():
                for value in dice_values:
                    if self.can_move_piece(color, piece.id, value):
                        movable_pieces.append((value, piece.id))

        return movable_pieces

    def can_move_piece(self, color, piece_id, steps):
        """Check if a piece can move the given number of steps."""
        piece = self.pieces[color][piece_id]
        current_pos = piece.get_position()

        # If in jail or in goal, can't move
        if piece.is_in_jail() or piece.is_in_goal():
            return False

        # Check if we're in final path
        if piece.is_in_final_path():
            new_pos = current_pos + steps

            # If exceeds goal, can't move
            if new_pos > self.goal_positions[color]:
                return False

            return True
        else:
            # Check if we would be blocked by a blockade
            # Calculate position after move (considering the circular path)
            new_pos = ((current_pos - 1 + steps) % 68) + 1

            # Check blockades along the path
            for pos in range(current_pos + 1, current_pos + steps + 1):
                check_pos = ((pos - 1) % 68) + 1
                if self.is_blockade(check_pos):
                    return False

            return True

    def count_pieces_in_jail(self, color):
        """Count how many pieces are in jail for a given color."""
        return sum(1 for piece in self.pieces[color] if piece.is_in_jail())