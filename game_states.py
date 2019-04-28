import enum

class GameStates(enum.Enum):
    """Class containing game states"""

    MAIN_MENU = 0
    PLAYING = 1
    PAUSE_MENU = 2
    GAME_OVER = 3
    SCORES = 4
