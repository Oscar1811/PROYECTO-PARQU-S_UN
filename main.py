import tkinter as tk
from parques import Parques


def main():
    """Function to initialize and run the game."""
    root = tk.Tk()
    root.title("Parqués UN")
    root.geometry("800x800")
    root.resizable(False, False)

    app = Parques(root)

    root.mainloop()


if __name__ == "__main__":
    main()