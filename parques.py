import tkinter as tk
from tkinter import messagebox
from tablero import Tablero
from dados import Dados
from fichas import GestorFichas
from jugador import GestorJugadores
from graficos import InterfazGrafica


class Parques:
    def __init__(self, master):
        """Initialize the game coordinator."""
        self.master = master
        self.num_players = 4

        # Initialize game components
        self.tablero = Tablero(master)
        self.dados = Dados(master)
        self.gestor_fichas = GestorFichas(self.num_players)
        self.gestor_jugadores = GestorJugadores(self.num_players)

        # Initialize graphical interface
        self.interfaz = InterfazGrafica(master, self)

        # Game state variables
        self.dice_values = [1, 1]
        self.movable_pieces = []
        self.bonus_moves = 0
        self.waiting_for_bonus_move = False
        self.turn_state = "roll"  # States: "roll", "select", "bonus", "end"

        # Setup dice roll button handler
        self.dados.roll_button.config(command=self.handle_dice_roll)

        # Show initial message
        self.interfaz.show_message("Parqués UN", "¡Bienvenido al juego de Parqués! Comienza el jugador Rojo.")

    def handle_dice_roll(self):
        """Handle dice roll action."""
        if self.turn_state == "roll":
            # Roll the dice
            self.dice_values = self.dados.roll()
            current_player = self.gestor_jugadores.get_current_player()

            # Check for pairs (same values)
            if self.dice_values[0] == self.dice_values[1]:
                pairs = current_player.add_consecutive_pair()
                if pairs == 3:
                    # Three consecutive pairs - send last moved piece to jail
                    last_moved = current_player.get_last_moved_piece()
                    if last_moved is not None:
                        self.gestor_fichas.get_piece(current_player.get_color(), last_moved).send_to_jail()
                        current_player.reset_consecutive_pairs()
                        self.interfaz.show_message("Tres pares consecutivos",
                                                   f"La ficha {last_moved + 1} vuelve a la cárcel.")
                    self.interfaz.update_display()
                else:
                    self.interfaz.show_message("Par", "¡Has sacado un par! Tendrás otro turno después de este.")
            else:
                # Reset consecutive pairs count
                current_player.reset_consecutive_pairs()

            # Find movable pieces with these dice values
            self.movable_pieces = self.gestor_fichas.get_movable_pieces(
                current_player.get_color(), self.dice_values
            )

            # Change state to select
            self.turn_state = "select"

            # Setup piece selection interface
            self.interfaz.setup_piece_selection(self.movable_pieces)

    def handle_piece_selection(self, dice_value, piece_id):
        """Handle piece selection action."""
        current_player = self.gestor_jugadores.get_current_player()
        current_color = current_player.get_color()

        if dice_value == -1:  # Release from jail
            # Find which die has a 5
            for i, value in enumerate(self.dice_values):
                if value == 5:
                    dice_index = i
                    break
            else:
                # If no 5, it means we have dice that sum to 5
                dice_index = -1

            # Release the piece from jail
            self.gestor_fichas.release_piece(current_color, piece_id)

            # Check if there's a piece to capture at the start position
            captured_color, captured_piece = self.gestor_fichas.check_start_position_capture(current_color)
            if captured_color is not None:
                self.interfaz.show_message("Captura",
                                           f"¡Has capturado una ficha del jugador {self.gestor_jugadores.get_player_by_color(captured_color).get_name()}!")
                self.bonus_moves = 20
                self.waiting_for_bonus_move = True

            # Remove the used die value
            if dice_index == -1:
                # Used both dice (sum of 5)
                self.dice_values = []
            else:
                # Used one die with value 5
                self.dice_values.pop(dice_index)
        else:
            # Regular move
            piece = self.gestor_fichas.get_piece(current_color, piece_id)
            old_position = piece.get_position()

            # Move the piece
            self.gestor_fichas.move_piece(current_color, piece_id, dice_value)

            # Set as last moved piece
            current_player.set_last_moved_piece(piece_id)

            # Check if the piece reached goal
            if piece.is_in_goal():
                self.interfaz.show_message("¡Llegada!", f"¡La ficha {piece_id + 1} ha llegado a la meta!")
                self.bonus_moves = 10
                self.waiting_for_bonus_move = True

                # Check for victory
                if self.gestor_fichas.all_pieces_in_goal(current_color):
                    self.interfaz.show_message("¡Victoria!",
                                               f"¡El jugador {current_player.get_name()} ha ganado!")
                    self.reset_game()
                    return

            # Check for captures (if not in final path)
            if not piece.is_in_final_path():
                new_position = piece.get_position()
                # Check if the position is not safe
                if new_position not in self.gestor_fichas.safe_positions and new_position not in self.gestor_fichas.start_positions.values():
                    captured_color, captured_piece = self.gestor_fichas.capture_piece(new_position, current_color)
                    if captured_color is not None:
                        self.interfaz.show_message("Captura",
                                                   f"¡Has capturado una ficha del jugador {self.gestor_jugadores.get_player_by_color(captured_color).get_name()}!")
                        self.bonus_moves = 20
                        self.waiting_for_bonus_move = True

            # Remove the used die value
            for i, value in enumerate(self.dice_values):
                if value == dice_value:
                    self.dice_values.pop(i)
                    break

        # Update the display
        self.interfaz.update_display()

        # Check if there are remaining dice values
        if not self.dice_values and not self.waiting_for_bonus_move:
            # End turn if no more dice and no bonus moves
            self.next_turn()
        elif not self.dice_values and self.waiting_for_bonus_move:
            # Switch to bonus moves
            self.turn_state = "bonus"
            self.process_bonus_move()
        else:
            # Continue with remaining dice
            self.movable_pieces = self.gestor_fichas.get_movable_pieces(
                current_color, self.dice_values
            )
            self.interfaz.setup_piece_selection(self.movable_pieces)

    def process_bonus_move(self):
        """Process bonus move (after capture or goal)."""
        current_player = self.gestor_jugadores.get_current_player()

        # Show bonus move message
        self.interfaz.show_message("Movimiento extra",
                                   f"Tienes {self.bonus_moves} movimientos extra. Selecciona una ficha y un dado.")

        # Find movable pieces with any value up to bonus_moves
        movable_with_bonus = []
        for i in range(1, min(self.bonus_moves + 1, 7)):  # Limited to 6 for UI
            pieces = self.gestor_fichas.get_movable_pieces(
                current_player.get_color(), [i]
            )
            movable_with_bonus.extend(pieces)

        # Setup piece selection for bonus move
        if movable_with_bonus:
            self.movable_pieces = movable_with_bonus
            self.interfaz.setup_piece_selection(self.movable_pieces)
        else:
            # No possible bonus moves
            self.interfaz.show_message("Sin movimientos extra",
                                       "No hay movimientos extra posibles. Fin del turno.")
            self.waiting_for_bonus_move = False
            self.bonus_moves = 0
            self.next_turn()

    def handle_bonus_move(self, dice_value, piece_id):
        """Handle bonus move selection."""
        current_player = self.gestor_jugadores.get_current_player()
        current_color = current_player.get_color()

        # Move the piece
        piece = self.gestor_fichas.get_piece(current_color, piece_id)
        self.gestor_fichas.move_piece(current_color, piece_id, dice_value)

        # Set as last moved piece
        current_player.set_last_moved_piece(piece_id)

        # Reduce bonus moves
        self.bonus_moves -= dice_value

        # Update the display
        self.interfaz.update_display()

        # Check if bonus moves are exhausted
        if self.bonus_moves <= 0:
            self.waiting_for_bonus_move = False
            self.next_turn()
        else:
            # Continue with remaining bonus moves
            self.process_bonus_move()

    def next_turn(self):
        """Move to the next player's turn."""
        # Reset turn state
        self.turn_state = "roll"
        self.dice_values = [1, 1]
        self.movable_pieces = []
        self.bonus_moves = 0
        self.waiting_for_bonus_move = False

        # Check if current player had pairs
        current_player = self.gestor_jugadores.get_current_player()
        if current_player.consecutive_pairs > 0 and current_player.consecutive_pairs < 3:
            # Player gets another turn
            self.interfaz.update_display()
            return

        # Move to next player
        next_player = self.gestor_jugadores.next_player()

        # Update the display
        self.interfaz.update_display()

        # Show next player message
        self.interfaz.show_message("Nuevo turno", f"Turno del jugador: {next_player.get_name()}")

    def reset_game(self):
        """Reset the game state."""
        # Reinitialize components
        self.gestor_fichas = GestorFichas(self.num_players)
        self.gestor_jugadores = GestorJugadores(self.num_players)

        # Reset game state
        self.dice_values = [1, 1]
        self.movable_pieces = []
        self.bonus_moves = 0
        self.waiting_for_bonus_move = False
        self.turn_state = "roll"

        # Update display
        self.interfaz.update_display()

        # Show initial message
        self.interfaz.show_message("Juego reiniciado", "¡Bienvenido al juego de Parqués! Comienza el jugador Rojo.")