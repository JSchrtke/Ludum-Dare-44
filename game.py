# TODO: make obstacles
# TODO: fix creatures respawning in the same rough area
# TODO: SCALE MAX CREATURE COUNT WITH TIME, POTENTIALLY SPEED ASWELL
# TODO: POTENTIALLY SCALE HEALTH LOSS WITH TIME ASWELL
#   use built in function to check for distance between sprites, so that the obstacles always have a gap large enough for the player in base state
# TODO: add graphics/assets
# TODO: make and add sound
# TODO: MAKE CREATURES STARTLE WHEN OTHERS GET KILLED, INCREASE THEIR SPEED
# TODO: IF TIME PERMITTING, MAKE actual healthbar
import arcade
import os
import random
import csv
from game_constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_NAME,
    PLAYER_MOVEMENT_SPEED,
    MAX_CREATURE_COUNT,
)
from game_states import GameStates
from background import Background
from menu import MainMenu, PauseMenu, GameOverMenu, ScoreBoard
from player import (
    Player,
    SPIN_ATTACK,
    SPIN_ATTACK_COST,
    FREEZE_ATTACK,
    FREEZE_ATTACK_COST,
    TELEPORT,
    TELEPORT_COST,
)
from creature import Moth


class Game(arcade.Window):
    """main game class"""

    def __init__(self, width, height, name):
        """Initialize the main game class.
        
        Parameters
        ----------
        width : int
            Window width
        height : int
            Window height
        name : str
            Window name
        """
        super().__init__(width, height, name)
        # init variable holding the state
        self.state = None
        # init variable holding the background
        self.background = None
        # init variable holding the menu
        self.main_menu = None
        self.pause_menu = None
        self.game_over_screen = None
        self.score_board = None
        # init variable holding the player
        self.player = None
        # list for all creature sprites
        self.all_creature_sprites_list = None

        # list for highscores
        self.high_scores = []

        # variable to check if state has changed
        self.state_change = None
        # variable for the new state, after state change
        self.new_state = None
        # previous state
        self.old_state = None

        # pause variable
        self.is_game_paused = True

    def setup(self):
        """Set up the game"""
        # set the default state
        self.state_change = False
        self.state = GameStates.MAIN_MENU

        # setup the background
        self.background = Background()
        self.background.center_x = SCREEN_WIDTH / 2
        self.background.center_y = SCREEN_HEIGHT / 2

        # setup the main menu
        self.main_menu = MainMenu()
        self.main_menu.center_x = SCREEN_WIDTH / 2
        self.main_menu.center_y = SCREEN_HEIGHT / 2

        # setup the pause menu
        self.pause_menu = PauseMenu()
        self.pause_menu.center_x = SCREEN_WIDTH / 2
        self.pause_menu.center_y = SCREEN_HEIGHT / 2

        # setup the game over screen
        self.game_over_screen = GameOverMenu()
        self.game_over_screen.center_x = SCREEN_WIDTH / 2
        self.game_over_screen.center_y = SCREEN_HEIGHT / 2

        # setup the highscores
        self.load_scores()

        # setup the scoreboard
        self.score_board = ScoreBoard()
        self.score_board.center_x = SCREEN_WIDTH / 2
        self.score_board.center_y = SCREEN_HEIGHT / 2

        # setup the player
        self.player = Player()
        self.player.center_x = SCREEN_WIDTH / 2
        self.player.center_y = SCREEN_HEIGHT / 2

        # setup the creatures
        self.all_creature_sprites_list = arcade.SpriteList()
        for i in range(MAX_CREATURE_COUNT):
            creature = Moth()
            creature.setup()
            self.all_creature_sprites_list.append(creature)

    def load_scores(self, file_path="scores.txt"):
        try:
            with open(file_path, "r") as file:
                for line in file:
                    self.high_scores.append(int(line.rstrip()))
        except FileNotFoundError:
            print("Error, couldn't find the score file.")

    def save_scores(self, file_path=None):
        if file_path is None:
            file_path = "scores.txt"

        with open(file_path, "w") as file:
            for value in self.high_scores:
                file.write(str(value) + "\n")

    def display_scores(self):
        score_pos_y = SCREEN_HEIGHT / 4 * 3
        font_size = 20
        for score in self.high_scores:
            score = str(score)
            arcade.draw_text(
                text=score,
                start_x=SCREEN_WIDTH / 2,
                start_y=score_pos_y,
                font_name="arial",
                font_size=font_size,
                color=arcade.color.BLACK,
                align="center",
                anchor_x="center",
                anchor_y="center",
            )
            score_pos_y += -font_size * 2

    def on_draw(self):
        """execute this code whenever window gets drawn"""
        arcade.start_render()
        self.background.draw()

        

        # when the game is in main_menu
        if self.state == GameStates.MAIN_MENU:
            self.main_menu.draw()

        # when the game is in the pause menu
        if self.state == GameStates.PAUSE_MENU:
            self.player.display_score(
                start_x=SCREEN_WIDTH / 2 - 100,
                start_y=SCREEN_HEIGHT / 2,
                font_size=50,
                bold=True,
            )
            self.player.display_health()
            self.pause_menu.draw()

        if self.state == GameStates.GAME_OVER:
            self.game_over_screen.draw()
            self.player.display_score(
                start_x=SCREEN_WIDTH / 2 - 100,
                start_y=SCREEN_HEIGHT / 2,
                font_size=50,
                bold=True,
            )


        if self.state == GameStates.SCORES:
            self.score_board.draw()
            self.high_scores = sorted(self.high_scores, reverse=True)
            self.display_scores()

        # when the game playing
        if self.state == GameStates.PLAYING:
            self.player.display_health()
            self.player.display_score(start_x=0, start_y=SCREEN_HEIGHT - 60)
            self.all_creature_sprites_list.draw()
            self.player.draw()
            if self.player.freeze_bullet is not None:
                self.player.freeze_bullet.draw()

    def on_update(self, delta_time):
        """Update the game"""
        if not self.is_game_paused:
            self.background.update()
            self.player.update()
            self.all_creature_sprites_list.update()

        if self.state == GameStates.PLAYING:
            # check if all creatures are gone, so new ones can be spawned
            if len(self.all_creature_sprites_list) <= 0:
                self.reset_all_creatures()

            if self.player.check_if_dead():
                self.set_state_change(True)
                self.set_new_state(GameStates.GAME_OVER)

            if self.player.has_hit_edge is True:
                if self.player.is_attacking is False:
                    self.background.set_texture_change_flag(True)
                    self.reset_all_creatures()

        if self.get_state_change() is True:
            self.set_state_change(False)
            self.set_old_state()
            self.update_state()

            # check if game is back to playing, if so, unpause game
            if self.state == GameStates.PLAYING:
                self.unpause_game()
            else:
                self.pause_game()

            if self.state == GameStates.MAIN_MENU:
                self.background.reset()
                self.high_scores.append(self.player.current_score)
                self.player.reset()
                self.reset_all_creatures()
                for creature in self.all_creature_sprites_list:
                    creature.reset_to_random_position()

            if self.state == GameStates.GAME_OVER:
                self.display_scores()

            if self.state == GameStates.SCORES:
                self.score_board.update()

    def on_key_press(self, symbol, modifiers):
        if self.state == GameStates.MAIN_MENU:
            if symbol == arcade.key.ENTER:
                self.set_state_change(True)
                self.set_new_state(GameStates.PLAYING)
            if symbol == arcade.key.TAB:
                self.set_state_change(True)
                self.set_new_state(GameStates.SCORES)
            if symbol == arcade.key.ESCAPE:
                self.quit()
                arcade.close_window()

        if self.state == GameStates.PLAYING:
            if symbol == arcade.key.ESCAPE:
                self.set_state_change(True)
                self.set_new_state(GameStates.PAUSE_MENU)
            if symbol == arcade.key.UP:
                self.player.move_up(PLAYER_MOVEMENT_SPEED)
            if symbol == arcade.key.DOWN:
                self.player.move_down(PLAYER_MOVEMENT_SPEED)
            if symbol == arcade.key.RIGHT:
                self.player.move_right(PLAYER_MOVEMENT_SPEED)
            if symbol == arcade.key.LEFT:
                self.player.move_left(PLAYER_MOVEMENT_SPEED)
            if symbol == arcade.key.SPACE:
                self.player.attack(self.all_creature_sprites_list)
            if symbol == arcade.key.A:
                self.player.select_attack_type(0)
            if symbol == arcade.key.S:
                self.player.select_attack_type(1)
            if symbol == arcade.key.D:
                self.player.select_attack_type(2)
            if symbol == arcade.key.F:
                self.player.select_attack_type(3)

        if self.state == GameStates.PAUSE_MENU:
            if symbol == arcade.key.ESCAPE:
                self.set_state_change(True)
                self.set_new_state(GameStates.MAIN_MENU)
            if symbol == arcade.key.ENTER:
                self.set_state_change(True)
                self.set_new_state(GameStates.PLAYING)
            if symbol == arcade.key.S:
                self.player.buy_attack(SPIN_ATTACK_COST, SPIN_ATTACK)
                print(
                    "spin attack count: {0}".format(
                        self.player.spin_attack_amount
                    )
                )  # TODO: DEBUG LINE, REMOVE
            if symbol == arcade.key.D:
                self.player.buy_attack(FREEZE_ATTACK_COST, FREEZE_ATTACK)
                print(
                    "freeze attack count: {0}".format(
                        self.player.freeze_attack_amount
                    )
                )  # TODO: DEBUG LINE, REMOVE
            if symbol == arcade.key.F:
                self.player.buy_attack(TELEPORT_COST, TELEPORT)
                print(
                    "teleport count: {0}".format(self.player.teleport_amount)
                )  # TODO: DEBUG LINE, REMOVE

        if self.state == GameStates.GAME_OVER:
            if symbol == arcade.key.ESCAPE:
                self.set_state_change(True)
                self.set_new_state(GameStates.MAIN_MENU)

        if self.state == GameStates.SCORES:
            if symbol == arcade.key.ESCAPE:
                self.set_state_change(True)
                self.set_new_state(self.old_state)

    def on_key_release(self, symbol, modifiers):
        if self.state == GameStates.PLAYING:
            # make the player stop moving in a certain direction when the
            # corresponding key is released
            if symbol == arcade.key.UP:
                self.player.move_up(0)
            if symbol == arcade.key.DOWN:
                self.player.move_down(0)
            if symbol == arcade.key.RIGHT:
                self.player.move_right(0)
            if symbol == arcade.key.LEFT:
                self.player.move_left(0)
            if symbol == arcade.key.SPACE:
                self.player.reset_after_attack()

    def set_state_change(self, boolean):
        """Set wether or not the state has changed.

        Parameters
        ----------
        boolean : Bool
            Boolean, wether the game state has changed.

        """
        self.state_change = boolean

    def get_state_change(self):
        """Get if the state of the game has changed.

        Returns
        -------
        bool
            Boolean, True when the game state has changed, else False

        """
        return self.state_change

    def set_new_state(self, new_state):
        """Set the next state the game should change to when updated.

        Parameters
        ----------
        new_state : GameState
            A state from the enum class GameState.

        """
        self.new_state = new_state

    def get_new_state(self):
        """Get the state the game will change to when updated.

        Returns
        -------
        GameState
            A state from the enum class GameState.

        """
        return self.new_state

    def set_old_state(self):
        """Set the old state to fall back to after state change"""
        self.old_state = self.state

    def update_state(self):
        """Update the game state to the new state."""
        self.state = self.new_state

    def reset_all_creatures(self):
        for creature in self.all_creature_sprites_list:
            creature.kill()
        for i in range(MAX_CREATURE_COUNT):
            creature = Moth()
            creature.setup()
            self.all_creature_sprites_list.append(creature)
            if len(self.all_creature_sprites_list) >= MAX_CREATURE_COUNT:
                break

    def pause_game(self):
        if not self.is_game_paused:
            self.is_game_paused = True
            for creature in self.all_creature_sprites_list:
                creature.pause_movement()

    def unpause_game(self):
        if self.is_game_paused:
            self.is_game_paused = False
            for creature in self.all_creature_sprites_list:
                creature.unpause_movement()

    def quit(self):
        self.save_scores()


def main():
    """Run the game"""
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_NAME)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
