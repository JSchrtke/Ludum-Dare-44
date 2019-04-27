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
        texture = arcade.load_texture(file_name="yellow.png")
        self.textures.append(texture)
        # set the default texture
        self.set_texture(0)
        self.texture_increment_counter = 0

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
            if self.texture_increment_counter < len(self.textures) - 1:
                self.texture_increment_counter += 1
            else:
                self.texture_increment_counter = 0

            self.set_texture(self.texture_increment_counter)
            self.set_texture_change_flag(False)


    def set_texture_change_flag(self, Boolean):
        """Set the texture change flas
        
        Parameters
        ----------
        Boolean : bool
            Wether the texture should be changed next update or not
        """
        self.change_texture_flag = Boolean

    def reset(self):
        self.texture_increment_counter = 0
        self.set_texture(0)
