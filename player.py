import arcade
import csv
from game_constants import SCREEN_WIDTH, SCREEN_HEIGHT

PLAYER_SCALE = 0.1
FACE_RIGHT = 0
FACE_LEFT = 1
BASE_ATTACK_RIGHT = 2
BASE_ATTACK_LEFT = 3
RIGHT = 0
LEFT = 180
UP = 90
DOWN = 270
MAX_HEALTH = 100
HEALTH_LOSS_PER_UPDATE = 100 / 3600
FONT_SIZE = 25


class Player(arcade.Sprite):
    """Class containing the player"""

    def __init__(self):
        super().__init__()
        # load the player texture
        texture = arcade.load_texture(
            file_name="pepe_facing_right.png", scale=PLAYER_SCALE
        )
        self.textures.append(texture)
        texture = arcade.load_texture(
            file_name="pepe_facing_left.png", scale=PLAYER_SCALE
        )
        self.textures.append(texture)
        texture = arcade.load_texture(
            file_name="pepe_facing_right_punching.png", scale=PLAYER_SCALE
        )
        self.textures.append(texture)
        texture = arcade.load_texture(
            file_name="pepe_facing_left_punching.png", scale=PLAYER_SCALE
        )
        self.textures.append(texture)

        # set the default texture
        self.set_texture(FACE_RIGHT)
        # variable to check if player has hit edge of screen
        self.has_hit_edge = False

        # health variables
        self.max_health = MAX_HEALTH
        self.current_health = MAX_HEALTH
        self.dead = False

        # list to save all the scores of the current game session, export to file later
        self.current_session_scores_list = []

        # score variables
        self.current_score = 0

    def update(self):
        """Update the player"""
        self.lose_health()
        self.has_hit_edge = False
        self.check_bounds()
        self.center_x += self.change_x
        self.center_y += self.change_y

    def reset(self):
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2
        self.current_health = self.max_health
        self.current_session_scores_list.append(self.current_score)
        self.current_score = 0
        self.dead = False


    def lose_health(self, amount=HEALTH_LOSS_PER_UPDATE):
        """Lose some health.
        
        Parameters
        ----------
        amount : float
            Health loss per update
        """
        self.current_health = self.current_health - HEALTH_LOSS_PER_UPDATE

    def check_if_dead(self):
        """Check if the player is dead"""
        if self.current_health <= 0:
            self.dead = True
            return self.dead

    def set_player_dead(self):
        if self.current_health <= 0:
            self.dead = True

    def move_right(self, speed):
        """Move the player to the right.
        
        Parameters
        ----------
        speed : int
            Movement speed in pixels per update
        """
        self.change_x = speed
        self.angle = RIGHT
        self.set_texture(FACE_RIGHT)

    def move_left(self, speed):
        """Move the player to the left.
        
        Parameters
        ----------
        speed : int
            Movement speed in pixels per update
        """
        self.change_x = -speed
        self.angle = LEFT
        self.set_texture(FACE_LEFT)

    def move_up(self, speed):
        """Move the player to the right.
        
        Parameters
        ----------
        speed : int
            Movement speed in pixels per update
        """
        self.change_y = speed
        self.angle = UP
        self.set_texture(FACE_RIGHT)

    def move_down(self, speed):
        """Move the player to the right.
        
        Parameters
        ----------
        speed : int
            Movement speed in pixels per update
        """
        self.change_y = -speed
        self.angle = DOWN
        self.set_texture(FACE_RIGHT)

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

    def base_attack(self, target_list):
        """Do a base attack.

        Parameters
        ----------
        target_list : arcade.SpriteList
            List of all the targets that can be attacked

        """
        dist = (
            self.textures[BASE_ATTACK_RIGHT].width / 2
            - self.textures[FACE_RIGHT].width / 2
        ) * PLAYER_SCALE
        self.translate_forward(dist)
        if self.angle == LEFT:
            self.set_texture(BASE_ATTACK_LEFT)
        else:
            self.set_texture(BASE_ATTACK_RIGHT)
        for target in arcade.check_for_collision_with_list(self, target_list):
            target.got_hit()
            if target.can_be_eaten:
                self.eat(target)
                target.got_eaten()

    def eat(self, target):
        self.current_health = self.current_health + target.value_when_eaten
        if self.current_health >= MAX_HEALTH:
            self.current_health = MAX_HEALTH

        self.current_score += target.score_when_eaten

    def display_score(
        self,
        start_x=(SCREEN_WIDTH / 2) - 15,
        start_y=SCREEN_HEIGHT / 2,
        font_size=FONT_SIZE,
        bold=False,
    ):
        current_score_str = str(self.current_score)
        arcade.draw_text(
            text="Score: {0}".format(current_score_str),
            start_x=start_x,
            start_y=start_y,
            color=arcade.color.BLACK,
            font_name="arial",
            font_size=font_size,
            bold=bold,
        )

    def display_health(self):
        current_health_str = str(round(self.current_health))
        arcade.draw_text(
            text="Health: {0}".format(current_health_str),
            start_x=0,
            start_y=SCREEN_HEIGHT - 30,
            color=arcade.color.BLACK,
            font_size=FONT_SIZE,
            font_name="arial",
        )

    def reset_after_attack(self):
        dist = (
            self.textures[BASE_ATTACK_RIGHT].width / 2
            - self.textures[FACE_RIGHT].width / 2
        ) * PLAYER_SCALE
        self.translate_forward(-dist)
        if self.angle == LEFT:
            self.set_texture(FACE_LEFT)
        else:
            self.set_texture(FACE_RIGHT)

    def translate_forward(self, distance):
        if self.angle == RIGHT:
            self.center_x = self.center_x + distance
        if self.angle == LEFT:
            self.center_x = self.center_x - distance
        if self.angle == UP:
            self.center_y = self.center_y + distance
        if self.angle == DOWN:
            self.center_y = self.center_y - distance

