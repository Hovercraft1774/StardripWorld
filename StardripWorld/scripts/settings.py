import os.path

import pygame as pg
import random


# define colors, colors work in a (RGB) format.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 115, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 0, 145)
YELLOW = (255,255,0)
TEAL = (0,255,255)
PINK = (255,0,255)
ORANGE = (255,127,0)
DARK_GRAY = (64,64,64)
LIGHT_GRAY = (192,192,192)
GRAY_BLUE = (92,192,194)
BGCOLOR = GREEN

colors = (WHITE,BLUE,BLACK,RED,GREEN,YELLOW,TEAL,PINK,ORANGE)



#Game Title
TITLE = "Stardrip World"
FONT_NAME = 'comic_sans'


# Window Settings
WIDTH =1024 # 16*64 or 32*32 or 64*16
HEIGHT = 768    #16*48 or 32*24 or 64*12
TILE_SIZE = 48
GRIDWIDTH = WIDTH/TILE_SIZE
GRIDHEIGHT = HEIGHT/TILE_SIZE

# camera settings
fps = 60

# file locations
#gets location of file on computer
game_folder = os.path.dirname(__file__)
game_folder = game_folder.replace("\scripts","")
sprites_folder = os.path.join(game_folder,"sprites")
playerSprites = os.path.join(sprites_folder,"playerSprites")
enemySprites = os.path.join(sprites_folder,"enemySprites")
background_folder = os.path.join(sprites_folder,"background")
snd_folder = os.path.join(game_folder,'snd_fx')
music_folder = os.path.join(snd_folder,'music')
MAIN_THEME = os.path.join(music_folder,'nature_sketch.wav')
CONFIRM_SOUND = os.path.join(snd_folder,'Confirm.wav')
BAD_SOUND = os.path.join(snd_folder,'Deny.wav')
COLLECT_SOUND = os.path.join(snd_folder,'collect.wav')

GRASS_BACKGROUND = os.path.join(background_folder,'grass_background.png')
MAP = os.path.join(background_folder, 'map.txt')

# player Settings
PLAYER_SPEED = 400
player_img = os.path.join(playerSprites,'george_single.png')


# SPRITESHEET = os.path.join(sprites_folder,'Spritesheet.png')


#items
wheat_img = os.path.join(playerSprites,'wheat.png')
milk_img = os.path.join(playerSprites, 'grass_milk.png')
grass_img = os.path.join(playerSprites,'grass.png')
water_tree_img = os.path.join(playerSprites,'water.png')
wall_img = os.path.join(playerSprites,'wall.png')
stone_img = os.path.join(playerSprites,'stone.png')
book_img = os.path.join(playerSprites,'book.png')
cake_img = os.path.join(playerSprites,'pink_cake.png')
apple_img = os.path.join(playerSprites,'grass_apple.png')
egg_img = os.path.join(playerSprites,'Fried Egg.png')
fire_img = os.path.join(playerSprites,'grass_fire.png')
tree_img = os.path.join(playerSprites,'grass_tree.png')
fish_img = os.path.join(playerSprites,'puffer.png')
cherry_img = os.path.join(playerSprites,'cherry_grass.png')
waterTree_img = os.path.join(playerSprites,'water_tree.png')
house_img = os.path.join(playerSprites,'grass_house.png')
lava_img = os.path.join(playerSprites,'lava.png')
water_img = os.path.join(playerSprites,'water.png')
strawberry_img = os.path.join(playerSprites,'grass_strawberry.png')
pepper_img = os.path.join(playerSprites,'grass_pepper.png')
coin_img = os.path.join(playerSprites,'coin.png')