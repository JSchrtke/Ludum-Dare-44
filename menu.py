import arcade

class MainMenu(arcade.Sprite):
    """The game menu"""

    def __init__(self):
        """Initialize menu sprite."""
        super().__init__()
        texture = arcade.load_texture(file_name="crude_menu.png")
        self.textures.append(texture)
        self.set_texture(0)

    def update(self):
        """Update the menu."""
        # if this needs updating, put the code here
        pass