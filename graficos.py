import tkinter as tk
from tkinter import messagebox


class InterfazGrafica:
    def __init__(self, master, parques):
        """Initialize the graphical interface."""
        self.master = master
        self.parques = parques

        # References to game components
        self.tablero = parques.tablero
        self.dados = parques.dados
        self.gestor_jugadores = parques.gestor_jugadores
        self.gestor_fichas = parques.gestor_fichas

        # Game status display
        self.status_frame = tk.Frame(master, bd=2, relief=tk.RIDGE)
        self.status_frame.place(x=10, y=10, width=780, height=60)

        self.status_label = tk.Label(self.status_frame, text="Parqués UN", font=("Arial", 16))
        self.status_label.pack(side=tk.TOP)

        self.turn_label = tk.Label(self.status_frame, text="Turno del jugador: Rojo", font=("Arial", 12))
        self.turn_label.pack(side=tk.TOP)

        # Game controls
        self.control_frame = tk.Frame(master, bd=2, relief=tk.RIDGE)
        self.control_frame.place(x=250, y=700, width=300, height=80)

        self.end_turn_button = tk.Button(self.control_frame, text="Finalizar Turno", command=self.end_turn)
        self.end_turn_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(self.control_frame, text="Reiniciar Juego", command=self.reset_game)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        # Setup action buttons
        self.piece_buttons = []

        # Highlights for movable pieces
        self.highlights = {}

        # Initial update
        self.update_display()

    def update_display(self):
        """Update the game display."""
        # Update turn indicator
        current_player = self.gestor_jugadores.get_current_player()
        self.turn_label.config(text=f"Turno del jugador: {current_player.get_name()}")

        # Update board with pieces
        self.tablero.draw_board()

        # Draw all pieces
        for color in range(self.parques.num_players):
            for piece in self.gestor_fichas.get_pieces_for_player(color):
                self.tablero.draw_piece(color, piece.id, piece.get_position())

    def highlight_movable_pieces(self, movable_pieces):
        """Highlight all movable pieces."""
        # Clear previous highlights
        for highlight_id in self.highlights.values():
            self.tablero.remove_highlight(highlight_id)
        self.highlights = {}

        # Add new highlights
        current_color = self.gestor_jugadores.get_current_player().get_color()

        for dice_value, piece_id in movable_pieces:
            if dice_value == -1:  # Release from jail
                piece = self.gestor_fichas.get_piece(current_color, piece_id)
                highlight_id = self.tablero.highlight_position(piece.get_position())
                self.highlights[(dice_value, piece_id)] = highlight_id
            else:
                piece = self.gestor_fichas.get_piece(current_color, piece_id)
                highlight_id = self.tablero.highlight_position(piece.get_position())
                self.highlights[(dice_value, piece_id)] = highlight_id

    def remove_highlights(self):
        """Remove all highlights."""
        for highlight_id in self.highlights.values():
            self.tablero.remove_highlight(highlight_id)
        self.highlights = {}

    def end_turn(self):
        """End the current player's turn."""
        self.parques.next_turn()

    def reset_game(self):
        """Reset the game."""
        if messagebox.askyesno("Reiniciar", "¿Estás seguro de reiniciar el juego?"):
            self.parques.reset_game()

    def show_message(self, title, message):
        """Display a message box."""
        messagebox.showinfo(title, message)

    def setup_piece_selection(self, movable_pieces):
        """Setup the interface for piece selection."""
        # Highlight movable pieces
        self.highlight_movable_pieces(movable_pieces)

        if not movable_pieces:
            self.show_message("Sin movimientos", "No hay movimientos posibles. Fin del turno.")
            self.parques.next_turn()
        else:
            # Wait for user click on a piece
            self.tablero.canvas.bind("<Button-1>", lambda event: self.handle_piece_click(event, movable_pieces))

    def handle_piece_click(self, event, movable_pieces):
        """Handle click on a piece."""
        x, y = event.x, event.y

        # Check if the click is on a highlighted piece
        for (dice_value, piece_id), highlight_id in self.highlights.items():
            current_color = self.gestor_jugadores.get_current_player().get_color()
            piece = self.gestor_fichas.get_piece(current_color, piece_id)

            # Get piece position
            if piece.is_in_jail():
                position = 0  # Jail
            else:
                position = piece.get_position()

            # Get piece coordinates
            if position == 0:  # In jail
                piece_coords = self.tablero.jail_positions[current_color][piece_id]
            else:
                piece_coords = self.tablero.board_positions[position]

            # Check if click is near the piece
            if abs(x - piece_coords[0]) < 25 and abs(y - piece_coords[1]) < 25:
                # Remove click handler and highlights
                self.tablero.canvas.unbind("<Button-1>")
                self.remove_highlights()

                # Process the move
                self.parques.handle_piece_selection(dice_value, piece_id)
                return

        # If click is not on a highlighted piece, do nothing