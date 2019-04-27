import arcade
from game_constants import SCREEN_WIDTH, SCREEN_HEIGHT
PLAYER_SCALE = 0.1


class Player(arcade.Sprite):
    """Class containing the player"""

    def __init__(self):
        super().__init__()
        # load the player texture
        texture = arcade.load_texture(file_name="pepe.png", scale=PLAYER_SCALE)
        self.textures.append(texture)
        self.set_texture(0)
        # variable to check if player has hit edge of screen
        self.has_hit_edge = False

    def update(self):
        """Update the player"""
        self.has_hit_edge = False
        self.check_bounds()
        self.center_x += self.change_x
        self.center_y += self.change_y

    def move_right(self, speed):
        """Move the player to the right.
        
        Parameters
        ----------
        speed : int
            Movement speed in pixels per update
        """
        self.change_x = speed

    def move_left(self, speed):
        """Move the player to the left.
        
        Parameters
        ----------
        speed : int
            Movement speed in pixels per update
        """
        self.change_x = -speed

    def move_up(self, speed):
        """Move the player to the right.
        
        Parameters
        ----------
        speed : int
            Movement speed in pixels per update
        """
        self.change_y = speed

    def move_down(self, speed):
        """Move the player to the right.
        
        Parameters
        ----------
        speed : int
            Movement speed in pixels per update
        """
        self.change_y = -speed

    def check_bounds(self):
        """Check if player is within allowed movement range."""
        # leaving screen on the left
        if self.left < 0:
            # change positon to move to a new "room"
            self.right = SCREEN_WIDTH - 1
            # set the edge check true
            self.has_hit_edge = True
        # leaving screen on the right
        if self.right > SCREEN_WIDTH - 1:
            # change positon to move to a new "room"
            self.left = 0
            # set the edge check true
            self.has_hit_edge = True
        # leaving screen on the bottom
        if self.bottom < 0:
            # change positon to move to a new "room"
            self.top = SCREEN_HEIGHT - 1
            # set the edge check true
            self.has_hit_edge = True
        if self.top > SCREEN_HEIGHT - 1:
            # change positon to move to a new "room"
            self.bottom = 0
            # set the edge check true
            self.has_hit_edge = True
