import tkinter as tk
from tkinter import Canvas
import math


class Tablero:
    def __init__(self, master, width=800, height=800):
        self.master = master

        self.width = width
        self.height = height
        self.canvas = Canvas(master, width=width, height=height, bg='white')
        self.canvas.pack()
        # Colors for each team
        self.colors = {
            0: '#FF0000',  # Red
            1: '#0000FF',  # Blue
            2: '#00FF00',  # Green
            3: '#FFFF00'  # Yellow
        }
        # Color names for display
        self.color_names = {
            0: 'Rojo',
            1: 'Azul',
            2: 'Verde',
            3: 'Amarillo'
        }
        # Start positions for each color
        self.start_positions = {
            0: 5,  # Red starts at position 5
            1: 22,  # Blue starts at position 22
            2: 39,  # Green starts at position 39
            3: 56  # Yellow starts at position 56
        }
        # Safe positions (general safe spots)
        self.safe_positions = [5, 12, 22, 29, 39, 46, 56, 63]
        # Home positions (the 8 squares before goal for each color)
        self.home_positions = {
            0: list(range(69, 77)),  # Red: 69-76
            1: list(range(77, 85)),  # Blue: 77-84
            2: list(range(85, 93)),  # Green: 85-92
            3: list(range(93, 101))  # Yellow: 93-100
        }
        # Goal positions
        self.goal_positions = {
            0: 76,  # Red's goal
            1: 84,  # Blue's goal
            2: 92,  # Green's goal
            3: 100  # Yellow's goal
        }
        # Jail positions for pieces
        self.jail_positions = {
            0: [(100, 100), (150, 100), (100, 150), (150, 150)],  # Red
            1: [(650, 100), (700, 100), (650, 150), (700, 150)],  # Blue
            2: [(650, 650), (700, 650), (650, 700), (700, 700)],  # Green
            3: [(100, 650), (150, 650), (100, 700), (150, 700)]  # Yellow
        }
        # Board positions (coordinates for each position)
        self.board_positions = self._calculate_board_positions()
        # Draw the board initially
        self.draw_board()

    def _calculate_board_positions(self):
        """Calculate the coordinates for each position on the board using a square layout."""
        positions = {}

        # Square layout parameters
        margin = 80  # Margin from the edge
        cell_size = 40  # Size of each cell

        # Calculate positions for the outer square (positions 1-68)
        # Each side of the square will have 17 positions (68/4 = 17)

        # Top side (left to right): positions 1-17
        for i in range(17):
            x = margin + i * cell_size
            y = margin
            positions[i + 1] = (x, y)

        # Right side (top to bottom): positions 18-34
        for i in range(17):
            x = margin + 16 * cell_size
            y = margin + i * cell_size
            positions[i + 18] = (x, y)

        # Bottom side (right to left): positions 35-51
        for i in range(17):
            x = margin + (16 - i) * cell_size
            y = margin + 16 * cell_size
            positions[i + 35] = (x, y)

        # Left side (bottom to top): positions 52-68
        for i in range(17):
            x = margin
            y = margin + (16 - i) * cell_size
            positions[i + 52] = (x, y)

        # Home paths for each color
        # Red home path (69-76)
        for i in range(8):
            positions[69 + i] = (150 + i * 50, 400)

        # Blue home path (77-84)
        for i in range(8):
            positions[77 + i] = (400, 150 + i * 50)

        # Green home path (85-92)
        for i in range(8):
            positions[85 + i] = (650 - i * 50, 400)

        # Yellow home path (93-100)
        for i in range(8):
            positions[93 + i] = (400, 650 - i * 50)

        return positions

    def draw_board(self):
        """Draw the complete board."""
        self.canvas.delete("all")
        # Draw the main board
        self._draw_external_path()
        self._draw_home_paths()
        self._draw_jails()
        self._draw_safe_spots()

    def _draw_external_path(self):
        """Draw the external path with 68 cells."""
        for pos in range(1, 69):
            x, y = self.board_positions[pos]
            # Change color for start positions
            if pos in self.start_positions.values():
                color_idx = list(self.start_positions.values()).index(pos)
                fill_color = self.colors[color_idx]
                self.canvas.create_rectangle(x - 20, y - 20, x + 20, y + 20, fill=fill_color, outline="black")
                self.canvas.create_text(x, y, text=str(pos), fill="white")
            # Safe positions
            elif pos in self.safe_positions:
                self.canvas.create_rectangle(x - 20, y - 20, x + 20, y + 20, fill="gray", outline="black")
                self.canvas.create_text(x, y, text=str(pos), fill="black")
            else:
                self.canvas.create_rectangle(x - 20, y - 20, x + 20, y + 20, fill="white", outline="black")
                self.canvas.create_text(x, y, text=str(pos), fill="black")

    def _draw_home_paths(self):
        """Draw the home paths for each color."""
        for color, positions in self.home_positions.items():
            for pos in positions:
                x, y = self.board_positions[pos]
                # Last position is the goal
                if pos == self.goal_positions[color]:
                    self.canvas.create_rectangle(x - 20, y - 20, x + 20, y + 20, fill=self.colors[color],
                                                 outline="black")
                    self.canvas.create_text(x, y, text="META", fill="white")
                else:
                    self.canvas.create_rectangle(x - 20, y - 20, x + 20, y + 20, fill=self.colors[color],
                                                 outline="black", width=1, stipple="gray50")
                    self.canvas.create_text(x, y, text=str(pos), fill="white")

    def _draw_jails(self):
        """Draw the jails for each team."""
        for color, positions in self.jail_positions.items():
            for i, (x, y) in enumerate(positions):
                self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill=self.colors[color], outline="black")
                self.canvas.create_text(x, y, text=f"{i + 1}", fill="white")

    def _draw_safe_spots(self):
        """Highlight the safe spots in the board."""
        for pos in self.safe_positions:
            x, y = self.board_positions[pos]
            self.canvas.create_oval(x - 25, y - 25, x + 25, y + 25, outline="black", width=2)

    def draw_piece(self, color, piece_id, position):
        """Draw a piece at the given position."""
        # If the piece is in jail
        if position == 0:
            jail_pos = self.jail_positions[color][piece_id]
            x, y = jail_pos
            self.canvas.create_oval(x - 12, y - 12, x + 12, y + 12, fill=self.colors[color], outline="black", width=2)
            self.canvas.create_text(x, y, text=str(piece_id + 1), fill="white")
        else:
            # If the piece is on the board
            x, y = self.board_positions[position]
            # Offset to avoid overlapping pieces
            if piece_id % 2 == 0:  # Pieces 0 and 2
                offset_x, offset_y = -10, -10 if piece_id == 0 else 10
            else:  # Pieces 1 and 3
                offset_x, offset_y = 10, -10 if piece_id == 1 else 10
            self.canvas.create_oval(x + offset_x - 10, y + offset_y - 10, x + offset_x + 10, y + offset_y + 10,
                                    fill=self.colors[color], outline="black", width=2)
            self.canvas.create_text(x + offset_x, y + offset_y, text=str(piece_id + 1), fill="white")

    def highlight_position(self, position):
        """Highlight a position to indicate it can be selected."""
        if position == 0:  # If it's in jail, we don't highlight
            return
        x, y = self.board_positions[position]
        highlight = self.canvas.create_rectangle(x - 23, y - 23, x + 23, y + 23, outline="yellow", width=3)
        return highlight

    def remove_highlight(self, highlight_id):
        """Remove the highlight."""
        self.canvas.delete(highlight_id)