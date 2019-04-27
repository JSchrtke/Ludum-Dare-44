import arcade
import os
from game_constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_NAME, PLAYER_MOVEMENT_SPEED
from game_states import GameStates
from background import Background
from menu import MainMenu
from player import Player


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
        self.menu = None
        # init variable holding the player
        self.player = None

        # variable to check if state has changed
        self.state_change = None
        # variable for the new state, after state change
        self.new_state = None
        # previous state
        self.old_state = None

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
        self.menu = MainMenu()
        self.menu.center_x = SCREEN_WIDTH / 2
        self.menu.center_y = SCREEN_HEIGHT / 2

        # setup the player
        self.player = Player()
        self.player.center_x = SCREEN_WIDTH / 2
        self.player.center_y = SCREEN_HEIGHT / 2

    def on_draw(self):
        """execute this code whenever window gets drawn"""
        arcade.start_render()
        self.background.draw()

        # when the game is in menu
        if self.state == GameStates.MAIN_MENU:
            self.menu.draw()

        # when the game playing
        if self.state == GameStates.PLAYING:
            self.player.draw()

    def on_update(self, delta_time):
        """Update the game"""
        self.background.update()
        self.player.update()
        # TODO: DEBUG CODE, REMOVE WHEN DONE
        #######################################################################
        # print(self.state)
        if self.state == GameStates.PLAYING:
            if self.player.has_hit_edge is True:
                self.background.set_texture_change_flag(True)
                print(self.player.has_hit_edge)
        # END OF DEBUG CODE
        #######################################################################
        if self.get_state_change() is True:
            self.set_state_change(False)
            self.set_old_state()
            self.update_state()

    def on_key_press(self, symbol, modifiers):
        if self.state == GameStates.MAIN_MENU:
            if symbol == arcade.key.ENTER:
                self.set_state_change(True)
                self.set_new_state(GameStates.PLAYING)
            if symbol == arcade.key.TAB:
                self.set_state_change(True)
                self.set_new_state(GameStates.SCORES)
            if symbol == arcade.key.ESCAPE:
                # TODO: make proper quite logic
                arcade.close_window()

        if self.state == GameStates.PLAYING:
            if symbol == arcade.key.ESCAPE:
                self.set_state_change(True)
                self.set_new_state(GameStates.INGAME_MENU)
                # TODO: make pause logic to pause game when in menu
            if symbol == arcade.key.UP:
                self.player.move_up(PLAYER_MOVEMENT_SPEED)
            if symbol == arcade.key.DOWN:
                self.player.move_down(PLAYER_MOVEMENT_SPEED)
            if symbol == arcade.key.RIGHT:
                self.player.move_right(PLAYER_MOVEMENT_SPEED)
            if symbol == arcade.key.LEFT:
                self.player.move_left(PLAYER_MOVEMENT_SPEED)

        if self.state == GameStates.INGAME_MENU:
            if symbol == arcade.key.ESCAPE:
                self.set_state_change(True)
                self.set_new_state(GameStates.MAIN_MENU)
            if symbol == arcade.key.ENTER:
                self.set_state_change(True)
                self.set_new_state(GameStates.PLAYING)
            if symbol == arcade.key.TAB:
                self.set_state_change(True)
                self.set_new_state(GameStates.SCORES)

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


def main():
    """Run the game"""
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_NAME)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
