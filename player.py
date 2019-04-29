import arcade
from game_constants import SCREEN_WIDTH, SCREEN_HEIGHT

PLAYER_SCALE = 0.1
FACE_RIGHT_TEXTURE = 0
FACE_LEFT_TEXTURE = 1
BASE_ATTACK_RIGHT_TEXTURE = 2
BASE_ATTACK_LEFT_TEXTURE = 3
SPIN_ATTACK_TEXTURE = 4
TELEPORT_TEXTURE = 5
RIGHT = 0
LEFT = 180
UP = 90
DOWN = 270
MAX_HEALTH = 100
HEALTH_LOSS_PER_UPDATE = 100 / 3600
FONT_SIZE = 25
BASE_ATTACK = 0
SPIN_ATTACK = 1
FREEZE_ATTACK = 2
TELEPORT = 3
SPIN_ATTACK_COST = 80
FREEZE_ATTACK_COST = 20
TELEPORT_COST = 5
BULLET_SPEED = 30
TELEPORT_DISTANCE = 400




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
        texture = arcade.load_texture(
            file_name="pepe_spin.png", scale=1
        )
        self.textures.append(texture)

        texture = arcade.load_texture(
            file_name="pepe_teleport.png", scale=PLAYER_SCALE
        )
        self.textures.append(texture)

        # init movement vars
        self.change_x = 0
        self.change_y = 0
        self.change_angle = 0

        # variables for handling the spinning attack
        self.is_spinning = False
        self.pos_before_spin = (0, 0)

        self.is_attacking = False

        # set the default texture
        self.set_texture(FACE_RIGHT_TEXTURE)
        # variable to check if player has hit edge of screen
        self.has_hit_edge = False

        # health variables
        self.max_health = MAX_HEALTH
        self.current_health = MAX_HEALTH
        self.dead = False

        # list to save all the scores of the current game session, export to file later
        self.current_session_scores_list = []

        # attack type variable
        self.current_attack_type = BASE_ATTACK

        self.freeze_bullet = None

        # attack count variables
        # TODO: SET THIS TO ZERO AGAIN
        self.spin_attack_amount = 0
        self.freeze_attack_amount = 0
        self.teleport_amount = 0

        # score variables
        self.current_score = 0

    def update(self):
        """Update the player"""
        if self.is_attacking is False:
            self.check_bounds()
        if self.freeze_bullet is not None:
            self.freeze_bullet.update()
        self.lose_health()
        # self.has_hit_edge = False
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle += self.change_angle

    def reset(self):
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2
        self.current_health = self.max_health
        self.current_session_scores_list.append(self.current_score)
        self.current_score = 0
        self.dead = False

    def select_attack_type(self, attack_type):
        """Select an attack type
        
        Parameters
        ----------
        attack_type : int
            0: base, 1: spin, 2: freeze, 3: teleport
        """
        # TODO: MAKE ENUMS FOR ATTACK TYPES, SO THE CODE LOOKS NICER
        self.current_attack_type = attack_type

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
        self.set_texture(FACE_RIGHT_TEXTURE)

    def move_left(self, speed):
        """Move the player to the left.
        
        Parameters
        ----------
        speed : int
            Movement speed in pixels per update
        """
        self.change_x = -speed
        self.angle = LEFT
        self.set_texture(FACE_LEFT_TEXTURE)

    def move_up(self, speed):
        """Move the player to the right.
        
        Parameters
        ----------
        speed : int
            Movement speed in pixels per update
        """
        self.change_y = speed
        self.angle = UP
        self.set_texture(FACE_RIGHT_TEXTURE)

    def move_down(self, speed):
        """Move the player to the right.
        
        Parameters
        ----------
        speed : int
            Movement speed in pixels per update
        """
        self.change_y = -speed
        self.angle = DOWN
        self.set_texture(FACE_RIGHT_TEXTURE)

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

    def buy_attack(self, cost, attack_type):
        if self.current_health - cost > 0:
            self.current_health += -cost

            if attack_type == SPIN_ATTACK:
                self.spin_attack_amount += 1
            if attack_type == FREEZE_ATTACK:
                self.freeze_attack_amount += 1
            if attack_type == TELEPORT:
                self.teleport_amount +=1


    def base_attack(self, target_list):
        """Do a base attack.

        Parameters
        ----------
        target_list : arcade.SpriteList
            List of all the targets that can be attacked

        """
        dist = (
            self.textures[BASE_ATTACK_RIGHT_TEXTURE].width / 2
            - self.textures[FACE_RIGHT_TEXTURE].width / 2
        ) * PLAYER_SCALE
        self.translate_forward(dist)
        if self.angle == LEFT:
            self.set_texture(BASE_ATTACK_LEFT_TEXTURE)
        else:
            self.set_texture(BASE_ATTACK_RIGHT_TEXTURE)
        for target in arcade.check_for_collision_with_list(self, target_list):
            target.got_hit()
            if target.can_be_eaten:
                self.eat(target)
                target.got_eaten()

    def spin_attack(self, target_list):
        """do spin attack"""
        # TODO: ADD CODE
        self.set_texture(SPIN_ATTACK_TEXTURE)
        self.change_angle = 15
        self.is_spinning = True
        
        for target in target_list:
            target.got_hit()
            if target.can_be_eaten:
                self.eat(target)
                target.got_eaten()


    def freeze_attack(self, target_list):
        """do freeze attack"""
        # TODO: ADD CODE
        self.freeze_bullet = arcade.Sprite(filename="freeze_bullet.png", scale=1, center_x=self.center_x, center_y=self.center_y)
        if self.angle == RIGHT:
            self.freeze_bullet.angle = RIGHT
            self.freeze_bullet.change_x = BULLET_SPEED
            self.freeze_bullet.left = self.right
        if self.angle == LEFT:
            self.freeze_bullet.angle = LEFT
            self.freeze_bullet.change_x =- BULLET_SPEED
            self.freeze_bullet.right = self.left
        if self.angle == UP:
            self.freeze_bullet.angle = UP
            self.freeze_bullet.change_y = BULLET_SPEED
            self.freeze_bullet.bottom = self.top
        if self.angle == DOWN:
            self.freeze_bullet.angle = DOWN
            self.freeze_bullet.change_y = -BULLET_SPEED
            self.freeze_bullet.top = self.bottom
        for target in arcade.check_for_collision_with_list(self.freeze_bullet, target_list):
            target.freeze()

    def teleport(self):
        """teleport forwards"""
        self.set_texture(TELEPORT_TEXTURE)
        if self.angle == RIGHT:
            self.center_x += TELEPORT_DISTANCE
        if self.angle == LEFT:
            self.center_x += -TELEPORT_DISTANCE
        if self.angle == UP:
            self.center_y += TELEPORT_DISTANCE
        if self.angle == DOWN:
            self.center_y += -TELEPORT_DISTANCE
        pass

    def attack(self, target_list):
        """Do selected attack"""
        self.is_attacking = True
        if (
            self.current_attack_type == SPIN_ATTACK
            and self.spin_attack_amount > 0
        ):
            self.spin_attack(target_list)
            self.spin_attack_amount += -1

        elif (
            self.current_attack_type == FREEZE_ATTACK
            and self.freeze_attack_amount > 0
        ):
            self.freeze_attack(target_list)
            self.freeze_attack_amount += -1

        elif self.current_attack_type == TELEPORT and self.teleport_amount > 0:
            self.teleport()
            self.teleport_amount += -1

        else:
            self.base_attack(target_list)

    def reset_after_attack(self):
        self.is_attacking = False
        if self.current_attack_type == SPIN_ATTACK:
            #self.is_spinning = False
            self.angle = 0
            self.change_angle = 0

        elif self.current_attack_type == FREEZE_ATTACK:
            pass

        elif self.current_attack_type == TELEPORT:
            pass

        else:
            dist = (
                self.textures[BASE_ATTACK_RIGHT_TEXTURE].width / 2
                - self.textures[FACE_RIGHT_TEXTURE].width / 2
            ) * PLAYER_SCALE

            self.translate_forward(-dist)
        # reset to base texture after attack
        if self.angle == LEFT:
            self.set_texture(FACE_LEFT_TEXTURE)
        else:
            self.set_texture(FACE_RIGHT_TEXTURE)
        # reset attack type to prevent missfires
        self.current_attack_type = BASE_ATTACK

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
            color=arcade.color.OUTRAGEOUS_ORANGE,
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
            color=arcade.color.OUTRAGEOUS_ORANGE,
            font_size=FONT_SIZE,
            font_name="arial",
        )

    def display_attack_counts(self):
        spin_attack_count = str(self.spin_attack_amount)
        freeze_attack_count = str(self.freeze_attack_amount)
        teleport_amount = str(self.teleport_amount)
        arcade.draw_text(
            text="Spin attack: {0}".format(spin_attack_count),
            start_x=200,
            start_y=SCREEN_HEIGHT - 30,
            color=arcade.color.OUTRAGEOUS_ORANGE,
            font_size=FONT_SIZE,
            font_name="arial",
        )
        arcade.draw_text(
            text="Freeze attack: {0}".format(freeze_attack_count),
            start_x=450,
            start_y=SCREEN_HEIGHT - 30,
            color=arcade.color.OUTRAGEOUS_ORANGE,
            font_size=FONT_SIZE,
            font_name="arial",
        )
        arcade.draw_text(
            text="Teleport: {0}".format(teleport_amount),
            start_x=750,
            start_y=SCREEN_HEIGHT - 30,
            color=arcade.color.OUTRAGEOUS_ORANGE,
            font_size=FONT_SIZE,
            font_name="arial",
        )

    def translate_forward(self, distance):
        if self.angle == RIGHT:
            self.center_x = self.center_x + distance
        if self.angle == LEFT:
            self.center_x = self.center_x - distance
        if self.angle == UP:
            self.center_y = self.center_y + distance
        if self.angle == DOWN:
            self.center_y = self.center_y - distance

    def stop(self):
        self.change_x = 0
        self.change_y = 0
