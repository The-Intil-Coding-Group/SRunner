"""
Program Name:           SRunner.py
Creator:                James Ashwood
Date last modified:     9 Aug 2021
Github Link:            https://github.com/The-Intil-Coding-Group/SRunner/
"""

### ~ Imports and variable definiitions ~ ###

## Imports

import arcade
from typing import Optional
import random

from arcade.window_commands import start_render

## Constants

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "SRunner"

GRAVITY = 1500

DEFAULT_DAMPING = 1.0
PLAYER_DAMPING = 0.8

PLAYER_FRICTION = 0.7
WALL_FRICTION = 0.7
DYNAMIC_ITEM_FRICTION = 0.6

PLAYER_MASS = 2.0

PLAYER_MAX_HORIZONTAL_SPEED = 1000
PLAYER_MAX_VERTICAL_SPEED = 1600

PLAYER_MOVE_FORCE_ON_GROUND = 45000

PLAYER_JUMP_IMPULSE = 1300

LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250

## Game specific data

global GAME_STATUS, CURRENT_BLOCK_NUMBER, CURRENT_BLOCK_TYPE, SCORE, BLOCKS, SELECTED, START_X

GAME_STATUS = 0

CURRENT_BLOCK_NUMBER = 1
CURRENT_BLOCK_TYPE = 0
SCORE = 1

BLOCKS = []

SELECTED = 2
START_X = 400

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        
        arcade.set_background_color((89, 89, 89))

        ### ~ Variable Definitions ~ ###
        
        self.player_list = None
        self.floor_list = None
        self.pool_list = None
        self.jumper_list = None
        self.player_sprite = None
        self.floor_sprite = None
        self.pool_sprite = None
        self.jumper_sprite = None
        self.physics_engine = Optional[arcade.PymunkPhysicsEngine]

    def setup(self):

        global GAME_STATUS, CURRENT_BLOCK_NUMBER, CURRENT_BLOCK_TYPE, SCORE, BLOCKS

        CURRENT_BLOCK_NUMBER = 1
        CURRENT_BLOCK_TYPE = 0
        SCORE = 1

        BLOCKS = []

        ### ~ Block generation ~ ###

        BLOCKS = [1, 1]
        potentialValues = [1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6]
        
        while len(BLOCKS) < 998:
            x = potentialValues[random.randint(0, len(potentialValues)-1)]
            if x != BLOCKS[-1]:
                BLOCKS.append(x)

        ### ~ Sprite Loading And Lists ~ ###

        ## Load up charecter

        self.start_list = arcade.SpriteList()
        image_sourceA ="code/resources/main.png"       ## Main player
        self.start_sprite = arcade.Sprite(image_sourceA, 2)
        self.start_sprite.center_x = 400
        self.start_sprite.center_y = 150
        self.start_list.append(self.start_sprite)
        image_sourceB ="code/resources/floor.png"       ## Floor
        self.start_sprite = arcade.Sprite(image_sourceB, 2)
        self.start_sprite.center_x = 500
        self.start_sprite.center_y = 60
        self.start_list.append(self.start_sprite)

        ## Player
        
        self.player_list = arcade.SpriteList()
        image_source ="code/resources/main.png"       ## Main player
        self.player_sprite = arcade.Sprite(image_source, 1)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)

        ## Create the floor list and add the sprites to it
        
        self.floor_list = arcade.SpriteList()
        image_source2 ="code/resources/floor.png"     ## Block type 1
        
        indexList = [i for i in range(len(BLOCKS)) if BLOCKS[i] == 1]
        valuesList = [i*240-120 for i in indexList]
        
        for x in valuesList:
            self.floor_sprite = arcade.Sprite(image_source2, 1.2)
            self.floor_sprite.center_x = x
            self.floor_sprite.center_y = 36
            self.floor_list.append(self.floor_sprite)

        ## Create the jumper list and add the sprites to it
            
        self.jumper_list = arcade.SpriteList()
        image_source3 ="code/resources/jumper.png"    ## Block type 2
        
        indexList = [i for i in range(len(BLOCKS)) if BLOCKS[i] == 2]
        valuesList = [i*240-120 for i in indexList]
        
        for x in valuesList:
            self.jumper_sprite = arcade.Sprite(image_source3, 1.2)
            self.jumper_sprite.center_x = x
            self.jumper_sprite.center_y = 57.6
            self.jumper_list.append(self.jumper_sprite)

        ## Create the hill list and add the sprites to it

        self.hill_list = arcade.SpriteList()
        image_source4 ="code/resources/hill.png"      ## Block type 3
        
        indexList = [i for i in range(len(BLOCKS)) if BLOCKS[i] == 3]
        valuesList = [i*240-120 for i in indexList]
        
        for x in valuesList:
            self.hill_sprite = arcade.Sprite(image_source4, 1.2)
            self.hill_sprite.center_x = x
            self.hill_sprite.center_y = 60
            self.hill_list.append(self.hill_sprite)

        ## Create the bridge list and add the sprites to it

        self.bridge_list = arcade.SpriteList()
        image_source4 ="code/resources/bridge.png"      ## Block type 4
        
        indexList = [i for i in range(len(BLOCKS)) if BLOCKS[i] == 4]
        valuesList = [i*240-120 for i in indexList]
        
        for x in valuesList:
            self.bridge_sprite = arcade.Sprite(image_source4, 1.2)
            self.bridge_sprite.center_x = x
            self.bridge_sprite.center_y = 36
            self.bridge_list.append(self.bridge_sprite)

        ## Create the pool list and add the sprites to it

        self.zapper_list = arcade.SpriteList()
        image_source4 ="code/resources/zapper.png"      ## Block type 5
        
        indexList = [i for i in range(len(BLOCKS)) if BLOCKS[i] == 5]
        valuesList = [i*240-120 for i in indexList]
        
        for x in valuesList:
            self.zapper_sprite = arcade.Sprite(image_source4, 1.2)
            self.zapper_sprite.center_x = x
            self.zapper_sprite.center_y = 60
            self.zapper_list.append(self.zapper_sprite)

        ## Block type 6 is the gap

        ## Background

        self.bg = arcade.SpriteList()

        for x in range(250):
            image_source6 ="code/resources/background.png"      ## Background
            self.bg_sprite = arcade.Sprite(image_source6, 1.2)
            self.bg_sprite.center_x = x * 600
            self.bg_sprite.center_y = 250
            self.bg.append(self.bg_sprite)

        ### ~ Physics Engine Setup ~ ###

        ## Set variables

        damping = DEFAULT_DAMPING
        gravity = (0, -GRAVITY)

        ## Run the functions to create the objects
        
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping, gravity=gravity)
        self.physics_engine.add_sprite(self.player_sprite, friction=PLAYER_FRICTION, mass=PLAYER_MASS, moment=arcade.PymunkPhysicsEngine.MOMENT_INF, collision_type="player", max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED, max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)
        self.physics_engine.add_sprite_list(self.floor_list, friction=0.6, collision_type="item", body_type=arcade.PymunkPhysicsEngine.STATIC)
        self.physics_engine.add_sprite_list(self.bridge_list, friction=0.1, collision_type="item", body_type=arcade.PymunkPhysicsEngine.STATIC)
        self.physics_engine.add_sprite_list(self.jumper_list, friction=0.6, collision_type="item", body_type=arcade.PymunkPhysicsEngine.STATIC)
        self.physics_engine.add_sprite_list(self.hill_list, friction=0.4, collision_type="item", body_type=arcade.PymunkPhysicsEngine.STATIC)
        self.physics_engine.add_sprite_list(self.zapper_list, friction=0.9, collision_type="item", body_type=arcade.PymunkPhysicsEngine.STATIC)

        self.view_left = 0 ## Scrolling Setup

    def on_draw(self):

        ### ~ Displaying The Game ~ ###
        
        global GAME_STATUS, SCORE, SELECTED
        arcade.start_render()

        ## Display the data based on the game status

        if GAME_STATUS == 0:
            arcade.draw_text("SRunner - Run for victory", 20, 525, arcade.color.BLACK, 50, font_name="code/resources/font.ttf")
            arcade.draw_text("Play", 20, 485, arcade.color.BLACK, 35, font_name="code/resources/font.ttf")
            arcade.draw_text("Help", 20, 445, arcade.color.BLACK, 35, font_name="code/resources/font.ttf")
            arcade.draw_text("Info", 20, 405, arcade.color.BLACK, 35, font_name="code/resources/font.ttf")
            arcade.draw_text("|", 5, ((40 * SELECTED) + 405), arcade.color.GREEN, 35, font_name="code/resources/font.ttf")
            self.start_list.draw()
        
        if GAME_STATUS == 1:
            self.bg.draw()
            self.floor_list.draw()
            self.player_list.draw()
            self.jumper_list.draw()
            self.hill_list.draw()
            self.zapper_list.draw()
            self.bridge_list.draw()
            
        if GAME_STATUS == 2:
            self.es = arcade.SpriteList()

            image_source7 ="code/resources/endscreen.png"      ## Background
            self.es_sprite = arcade.Sprite(image_source7, 1.8)
            self.es_sprite.center_x = 400
            self.es_sprite.center_y = 300
            self.es.append(self.es_sprite)
            self.es.draw()
            
            #arcade.draw_text("Game over, you score was " + str(SCORE) + ". Click to restart.", 20, 20, arcade.color.BLACK, 30, font_name="code/resources/font.ttf")

    def on_update(self, delta_time):

        ## Check for the right game status        
        global GAME_STATUS, CURRENT_BLOCK_NUMBER, CURRENT_BLOCK_TYPE, SCORE, BLOCKS, START_X

        if GAME_STATUS == 0:
            for sprite in self.start_list:
                sprite.center_x = sprite.center_x + 1
                if sprite.center_x > 1000:
                    for sprite in self.start_list:
                        sprite.center_x = sprite.center_x - 1200

        if GAME_STATUS == 1:

            self.physics_engine.step()  ## Update the physics engine

            ### ~ Scrolling ~ ###

            changed = False

            ## Check if the player is moving towards the edges, if so then move the viewport values and update the changed variable

            left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
            if self.player_sprite.left < left_boundary:
                self.view_left -= left_boundary - self.player_sprite.left
                changed =  True
                
            right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
            if self.player_sprite.right > right_boundary:
                self.view_left += self.player_sprite.right - right_boundary
                changed = True

            ## If it has changed, write out the thing
                
            if changed:
                self.view_l = int(self.view_left)

                arcade.set_viewport(self.view_left,
                                    SCREEN_WIDTH + self.view_left,
                                    -50,
                                    SCREEN_HEIGHT-50)

            ### ~ Super Jump and Zapper block ~ ###

            SCORE = round(self.player_sprite.center_x / 240)
            CURRENT_BLOCK_NUMBER = SCORE
            CURRENT_BLOCK_TYPE = BLOCKS[CURRENT_BLOCK_NUMBER]
            
            if CURRENT_BLOCK_TYPE == 2:     ## Check for super jump block
                if self.physics_engine.is_on_ground(self.player_sprite):  ## Check if the player is on the ground
                    impulse = (0, PLAYER_JUMP_IMPULSE*2)        ## Make it jump twice the normal height
                    self.physics_engine.apply_impulse(self.player_sprite, impulse)  ## Apply the jump impulse

            if CURRENT_BLOCK_TYPE == 5:     ## Check for zapper block
                if self.physics_engine.is_on_ground(self.player_sprite):  ## Check if the player is on the ground
                    impulse = (PLAYER_JUMP_IMPULSE*5, PLAYER_JUMP_IMPULSE)        ## Make it jump twice the normal height
                    self.physics_engine.apply_impulse(self.player_sprite, impulse)  ## Apply the jump impulse
            

        ### ~ Preparing the game status ~ ###

        if self.player_sprite.center_y < -400:
            GAME_STATUS = 2
            
            arcade.set_viewport(0,
                                SCREEN_WIDTH,
                                0,
                                SCREEN_HEIGHT)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        global GAME_STATUS

        if GAME_STATUS == 2:
            self.setup()
            GAME_STATUS = 1

    ### ~ Player Movement ~ ###


    def on_key_press(self, key, modifiers):

        global CURRENT_BLOCK_TYPE, GAME_STATUS, SELECTED

        if GAME_STATUS == 1:

            ## Player jumps if the UP or W key is pressed
            
            if key == arcade.key.UP or key == arcade.key.W:
                if self.physics_engine.is_on_ground(self.player_sprite):  ## Check if the player is on the ground
                    impulse = (0, PLAYER_JUMP_IMPULSE)
                    self.physics_engine.apply_impulse(self.player_sprite, impulse)  ## Apply the jump impulse

            ## If the player moves left or right, apply a force in that direction and turn off friction for the time being
                    
            elif key == arcade.key.LEFT or key == arcade.key.A:
                force = (-PLAYER_MOVE_FORCE_ON_GROUND, 0)
                self.physics_engine.apply_force(self.player_sprite, force)
                self.physics_engine.set_friction(self.player_sprite, 0)
                
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
                self.physics_engine.apply_force(self.player_sprite, force)
                self.physics_engine.set_friction(self.player_sprite, 0)

        if GAME_STATUS == 0:
            if key == arcade.key.UP or key == arcade.key.W:
                SELECTED += 1
                if SELECTED > 2:
                    SELECTED = 0
            if key == arcade.key.DOWN or key == arcade.key.S:
                SELECTED -= 1
                if SELECTED < 0:
                    SELECTED = 2
            if (key == arcade.key.SPACE or key == arcade.key.ENTER) and (SELECTED == 2):
                GAME_STATUS = 1
                self.setup()
            
    def on_key_release(self, key, key_modifiers):

        ## When the keys is release, start the friction again
        
        if key in [arcade.key.RIGHT, arcade.key.D, arcade.key.LEFT, arcade.key.A]:
            self.physics_engine.set_friction(self.player_sprite, 0.4)

### ~ Running The Game ~ ###

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
