import arcade
from game_constants import SCREEN_HEIGHT, SCREEN_WIDTH


class MainMenu(arcade.Sprite):
    """The game menu"""

    def __init__(self):
        """Initialize menu sprite."""
        super().__init__()
        texture = arcade.load_texture(file_name="main_menu.png")
        self.textures.append(texture)
        self.set_texture(0)

    def update(self):
        """Update the menu."""
        # if this needs updating, put the code here
        pass




class PauseMenu(arcade.Sprite):
    """The pause menu"""

    def __init__(self):
        super().__init__()
        texture = arcade.load_texture(file_name="pause_menu.png")
        self.textures.append(texture)
        self.set_texture(0)

    def update(self):
        pass


class GameOverMenu(arcade.Sprite):
    """The game over screen/menu"""

    def __init__(self):
        super().__init__()
        texture = arcade.load_texture(file_name="game_over.png")
        self.textures.append(texture)
        self.set_texture(0)


class ScoreBoard(arcade.Sprite):
    """The game over screen/menu"""

    def __init__(self):
        super().__init__()
        texture = arcade.load_texture(file_name="score_board.png")
        self.textures.append(texture)
        self.set_texture(0)
