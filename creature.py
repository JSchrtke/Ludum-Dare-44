import arcade
import random
from game_constants import SCREEN_WIDTH, SCREEN_HEIGHT

CREATURE_SCALE = 0.08
DEFAULT_HEALTH_VALUE_WHEN_EATEN = 10
DEFAULT_SCORE_VALUE_WHEN_EATEN = 1
CREATURE_SPEED = 10
ALIVE = 0
DEAD = 1
FROZEN = 2

# TODO: FIGURE OUT HOW TO TO THE CLASS INHERITANC STUFF PROPERLY, CONCERNING VALUES WHEN EATEN AND OTHER POTENTIAL PROPERTIES
class Creature(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.value_when_eaten = DEFAULT_HEALTH_VALUE_WHEN_EATEN
        self.score_when_eaten = DEFAULT_SCORE_VALUE_WHEN_EATEN
        self.moving = random.randint(0, 1)
        self.dead = False
        self.can_be_eaten = False
        self.can_be_eaten_increment_counter = 0

    def update(self):
        if self.dead:
            self.set_texture(DEAD)
            self.stop()
            self.can_be_eaten_increment_counter += 1
        if self.can_be_eaten_increment_counter == 6:
            self.can_be_eaten = True
            self.can_be_eaten_increment_counter = 0
        self.check_bounds()
        self.center_x += self.change_x
        self.center_y += self.change_y

    def setup(self):
        if self.moving == 1:
            self.change_x = CREATURE_SPEED * random.uniform(-0.5, 0.5)
            self.change_y = CREATURE_SPEED * random.uniform(-0.5, 0.5)

    def move_right(self, speed):
        """Move the creature to the right.
        
        Parameters
        ----------
        speed : int
            Movement speed in pixels per update
        """
        self.change_x = speed

    def move_left(self, speed):
        """Move the creature to the left.
        
        Parameters
        ----------
        speed : int
            Movement creature in pixels per update
        """
        self.change_x = -speed

    def move_up(self, speed):
        """Move the creature to the right.
        
        Parameters
        ----------
        speed : int
            Movement speed in pixels per update
        """
        self.change_y = speed

    def move_down(self, speed):
        """Move the creature to the right.
        
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
            # put player back to left edge
            self.left = 0
            # stop movement
            self.change_x = CREATURE_SPEED * random.uniform(0, 1)
            self.change_y = CREATURE_SPEED * random.uniform(-0.5, 0.5)
        # leaving screen on the right
        if self.right > SCREEN_WIDTH - 1:
            # put player back to right edge
            self.right = SCREEN_WIDTH - 1
            self.change_x = -CREATURE_SPEED * random.uniform(0, 1)
            self.change_y = CREATURE_SPEED * random.uniform(-0.5, 0.5)
        # leaving screen on the bottom
        if self.bottom < 0:
            # put player back to bottom edge
            self.bottom = 0
            self.change_y = CREATURE_SPEED * random.uniform(0, 1)
            self.change_x = CREATURE_SPEED * random.uniform(-0.5, 0.5)
        if self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1
            self.change_y = -CREATURE_SPEED * random.uniform(0, 1)
            self.change_x = CREATURE_SPEED * random.uniform(-0.5, 0.5)

    def pause_movement(self):
        self.change_x = 0
        self.change_y = 0
        self.change_angle = 0

    def unpause_movement(self):
        self.change_x = CREATURE_SPEED * random.uniform(-0.5, 0.5)
        self.change_y = CREATURE_SPEED * random.uniform(-0.5, 0.5)

    def reset_to_random_position(self):
        self.center_x = SCREEN_WIDTH / random.uniform(1, 10)
        self.center_y = SCREEN_HEIGHT / random.uniform(1, 10)

    def got_hit(self):
        self.dead = True

    def got_eaten(self):
        self.kill()

    def stop(self):
        self.change_x = 0
        self.change_y = 0

    def freeze(self):
        self.set_texture(FROZEN)
        self.stop()


class Moth(Creature):
    def __init__(self):
        super().__init__()
        # load default texture
        texture = arcade.load_texture(
            file_name="moth.png", scale=CREATURE_SCALE
        )
        self.textures.append(texture)
        # load texture for when the creature is dead
        texture = arcade.load_texture(
            file_name="moth_dead.png", scale=CREATURE_SCALE
        )
        self.textures.append(texture)
        texture = arcade.load_texture(
            file_name="moth_frozen.png", scale=CREATURE_SCALE
        )
        self.textures.append(texture)
        # set default texture
        self.set_texture(ALIVE)
        self.value_when_eaten = DEFAULT_HEALTH_VALUE_WHEN_EATEN * 2

        self.center_x = SCREEN_WIDTH / random.uniform(1, 10)
        self.center_y = SCREEN_HEIGHT / random.uniform(1, 10)

        
