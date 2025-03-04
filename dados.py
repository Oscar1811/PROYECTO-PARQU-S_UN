import random
import tkinter as tk
from tkinter import Canvas


class Dados:
    def __init__(self, master, x=400, y=400, size=50):
        """Initialize the dice system."""
        self.master = master
        self.x = x
        self.y = y
        self.size = size
        self.values = [1, 1]  # Default values for the two dice
        self.is_developer_mode = False

        # Create canvas for dice
        self.canvas = Canvas(master, width=size * 3, height=size * 1.5, bg='lightgray')
        self.canvas.place(x=x - size * 1.5, y=y - size * 0.75)

        # Draw initial dice
        self.draw_dice()

        # Button to roll dice
        self.roll_button = tk.Button(master, text="Lanzar Dados", command=self.roll)
        self.roll_button.place(x=x - 40, y=y + 50)

        # Developer mode widgets
        self.dev_frame = tk.Frame(master)
        self.dev_mode_var = tk.BooleanVar(value=False)
        self.dev_mode_check = tk.Checkbutton(
            master, text="Modo Desarrollador", variable=self.dev_mode_var,
            command=self.toggle_dev_mode
        )
        self.dev_mode_check.place(x=x - 60, y=y + 80)

        self.dice1_var = tk.StringVar(value="1")
        self.dice2_var = tk.StringVar(value="1")

        self.dice1_entry = tk.Entry(master, textvariable=self.dice1_var, width=2)
        self.dice2_entry = tk.Entry(master, textvariable=self.dice2_var, width=2)

        # Hide developer mode inputs initially
        self.dice1_entry.place_forget()
        self.dice2_entry.place_forget()

    def toggle_dev_mode(self):
        """Toggle developer mode on/off."""
        self.is_developer_mode = self.dev_mode_var.get()
        if self.is_developer_mode:
            self.dice1_entry.place(x=self.x - 60, y=self.y + 110)
            self.dice2_entry.place(x=self.x + 20, y=self.y + 110)
        else:
            self.dice1_entry.place_forget()
            self.dice2_entry.place_forget()

    def roll(self):
        """Roll the dice and get new values."""
        if self.is_developer_mode:
            try:
                dice1 = int(self.dice1_var.get())
                dice2 = int(self.dice2_var.get())

                # Validate the values are between 1 and 6
                if 1 <= dice1 <= 6 and 1 <= dice2 <= 6:
                    self.values = [dice1, dice2]
                else:
                    self.values = [random.randint(1, 6), random.randint(1, 6)]
            except ValueError:
                self.values = [random.randint(1, 6), random.randint(1, 6)]
        else:
            self.values = [random.randint(1, 6), random.randint(1, 6)]

        self.draw_dice()
        return self.values

    def draw_dice(self):
        """Draw the dice with their current values."""
        self.canvas.delete("all")

        # Draw first die
        self.draw_die(self.size // 2 + self.size // 4, self.size // 2, self.values[0])

        # Draw second die
        self.draw_die(self.size // 2 + self.size * 2 - self.size // 4, self.size // 2, self.values[1])

    def draw_die(self, x, y, value):
        """Draw a die with the given value at position (x, y)."""
        # Draw die outline
        self.canvas.create_rectangle(x - self.size // 2, y - self.size // 2,
                                     x + self.size // 2, y + self.size // 2,
                                     fill="white", outline="black")

        # Draw the dots based on value
        dot_radius = self.size // 10

        if value in [1, 3, 5]:  # Center dot
            self.canvas.create_oval(x - dot_radius, y - dot_radius,
                                    x + dot_radius, y + dot_radius,
                                    fill="black")

        if value in [2, 3, 4, 5, 6]:  # Top-left and bottom-right dots
            offset = self.size // 4
            self.canvas.create_oval(x - offset - dot_radius, y - offset - dot_radius,
                                    x - offset + dot_radius, y - offset + dot_radius,
                                    fill="black")
            self.canvas.create_oval(x + offset - dot_radius, y + offset - dot_radius,
                                    x + offset + dot_radius, y + offset + dot_radius,
                                    fill="black")

        if value in [4, 5, 6]:  # Top-right and bottom-left dots
            offset = self.size // 4
            self.canvas.create_oval(x + offset - dot_radius, y - offset - dot_radius,
                                    x + offset + dot_radius, y - offset + dot_radius,
                                    fill="black")
            self.canvas.create_oval(x - offset - dot_radius, y + offset - dot_radius,
                                    x - offset + dot_radius, y + offset + dot_radius,
                                    fill="black")

        if value == 6:  # Middle-left and middle-right dots
            offset = self.size // 4
            self.canvas.create_oval(x - offset - dot_radius, y - dot_radius,
                                    x - offset + dot_radius, y + dot_radius,
                                    fill="black")
            self.canvas.create_oval(x + offset - dot_radius, y - dot_radius,
                                    x + offset + dot_radius, y + dot_radius,
                                    fill="black")

    def get_values(self):
        """Return the current dice values."""
        return self.values

    def disable(self):
        """Disable dice rolling."""
        self.roll_button.config(state="disabled")

    def enable(self):
        """Enable dice rolling."""
        self.roll_button.config(state="normal")