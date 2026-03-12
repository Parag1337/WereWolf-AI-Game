"""
Animated Werewolf / Mafia Simulation

This version renders the game as a scene-driven animated experience.
It uses Tkinter for rendering and features AI players with suspicion mechanics,
voice dialogue, and a real game loop using root.after().

Run this script to start the game:
    python main.py

Controls:
    F5          - Next phase
    F6          - Toggle auto play
    F2          - New game
    Space       - Next phase
    Click name  - Select player
"""

import tkinter as tk

from ui import GameUI


def main() -> None:
    """Start the game."""
    root = tk.Tk()
    GameUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
