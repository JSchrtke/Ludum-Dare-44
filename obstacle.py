import arcade
import random
OBSTACLE_TEXTURE_COUNT = 2
from game_constants import SCREEN_WIDTH, SCREEN_HEIGHT
PINECONE_SCALE = 0.06
ROCK_SCALE = 0.02
LEAF_SCALE = 0.02

class Obstacle(arcade.Sprite):
    def __init__(self):
        super().__init__()
        rand_int = random.randint(0, OBSTACLE_TEXTURE_COUNT)
        texture = arcade.load_texture(file_name="pinecone.png", scale= PINECONE_SCALE)
        self.textures.append(texture)
        texture = arcade.load_texture(file_name="rock.png", scale= ROCK_SCALE)
        self.textures.append(texture)
        texture = arcade.load_texture(file_name="leaf.png", scale= LEAF_SCALE)
        self.textures.append(texture)
        self.set_texture(rand_int)

        self.has_hit_edge = False

    def setup(self):
        self.randomize_position()

    def update(self):
        self.check_bounds()

    def randomize_position(self):
        rand_float_1 = random.uniform(0, 1)
        rand_float_2 = random.uniform(0, 1)
        self.center_x = SCREEN_WIDTH * rand_float_1
        self.center_y = SCREEN_HEIGHT * rand_float_2
        self.angle = 90 * random.randint(1,4)

    def check_bounds(self):
        """Check if obstacle is within allowed range."""
        # leaving screen on the left
        if self.left < 0:
            self.center_x += self.collision_radius
        # leaving screen on the right
        if self.right > SCREEN_WIDTH - 1:
            self.center_x += -self.collision_radius
        # leaving screen on the bottom
        if self.bottom < 0:
            self.center_y += self.collision_radius
        if self.top > SCREEN_HEIGHT - 1:
            self.center_y += -self.collision_radius