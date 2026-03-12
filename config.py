"""
Configuration and constants for the Werewolf game.
"""

import os

# Color palette
COLORS = {
    "bg": "#171821",
    "panel": "#202231",
    "panel2": "#26293a",
    "surface": "#2d3146",
    "surface2": "#353a52",
    "text": "#e7ebff",
    "muted": "#97a0c3",
    "red": "#ff6f7d",
    "green": "#72e0a1",
    "yellow": "#ffd36b",
    "blue": "#77b8ff",
    "cyan": "#71e8ff",
    "purple": "#b89bff",
    "orange": "#ffae70",
    "black": "#08090d",
}

# Asset paths
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
ASSET_VARIANTS = {
    "day": ["dayBackground.png", "dayBackround.png"],
    "night": ["nightBackground.png", "nightBackround.png"],
    "villager": ["villager.png"],
    "werewolf": ["werewolf.png"],
    "bonefire": ["bonefire.png"],
}

# Role and dialogue colors
ROLE_COLORS = {
    "Villager": COLORS["text"],
    "Werewolf": COLORS["red"],
    "Doctor": COLORS["green"],
    "Detective": COLORS["blue"],
}

LOG_TAGS = {
    "system": COLORS["muted"],
    "speech": COLORS["text"],
    "accuse": COLORS["yellow"],
    "defend": COLORS["orange"],
    "reveal": COLORS["blue"],
    "vote": COLORS["cyan"],
    "kill": COLORS["red"],
    "save": COLORS["green"],
}

SPEECH_COLORS = {
    "info": COLORS["surface2"],
    "accuse": "#3b3348",
    "defend": "#43372f",
    "reveal": "#23384c",
}

# UI Layout
SIDEBAR_LEFT_WIDTH = 240
SIDEBAR_RIGHT_WIDTH = 300
AVATAR_SIZE = 48
AVATAR_SIZE_SCENE = (56, 108)  # (min, max)
GAME_WINDOW_SIZE = "1440x900"
GAME_WINDOW_MIN_SIZE = (1280, 780)

# Game constants
DEFAULT_PLAYER_COUNT = 8
ANIMATION_FRAME_RATE = 33  # milliseconds
AUTO_PLAY_DELAY = 0.9  # seconds
