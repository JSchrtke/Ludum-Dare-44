import arcade
import random


class Background(arcade.Sprite):
    """Class containing the background"""

    def __init__(self):
        super().__init__()
        # load all the textures for different backgrounds
        texture = arcade.load_texture(file_name="red.png")
        self.textures.append(texture)
        texture = arcade.load_texture(file_name="green.png")
        self.textures.append(texture)
        # set the default texture
        self.set_texture(0)

        # variable to check if texture needs changing
        self.change_texture_flag = False

    def update(self):
        self.change_texture()

    def select_random_texture(self):
        """select a random texture from the list of textures"""
        rand_int = random.randint(0, len(self.textures) - 1)
        self.set_texture(rand_int)

    def change_texture(self):
        """Changes the texture"""
        if self.change_texture_flag is True:
            self.select_random_texture()
            self.change_texture_flag = False
