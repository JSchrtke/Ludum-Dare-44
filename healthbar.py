import arcade
from game_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import MAX_HEALTH, HEALTH_LOSS_PER_UPDATE


class HealthBar():
    def __init__(self):
        self.max_width = (MAX_HEALTH * 5) * 2
        self.current_width = MAX_HEALTH * 5
        self.height = SCREEN_HEIGHT / 15
        self.center_x = 0
        self.center_y = self.height / 2 + 10
        self.colour = arcade.color.SHOCKING_PINK
        self.change_x = HEALTH_LOSS_PER_UPDATE

    def update(self, player):
        self.current_width = self.current_width - HEALTH_LOSS_PER_UPDATE * 5
        # self.center_x += -self.change_x

    def draw(self):
        arcade.draw_rectangle_filled(
            center_x=self.center_x,
            center_y=self.center_y,
            width=self.current_width,
            height=self.height,
            color=self.colour,
        )
