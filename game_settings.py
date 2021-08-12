import pygame as pg
from user_settings import *
vec = pg.math.Vector2

# Define colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)

# Game settings
TITLE = 'HoMM Dungeons'
BGCOLOR = BROWN


TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE


# Player settings
PLAYER_HEALTH = 150
PLAYER_STAMINA = 100
PLAYER_MAGIC = 100
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'warlock2.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
PLAYER_STAMINA_REGEN = 5
PLAYER_RAGE = 300
MISSLE_OFFSET = vec(30, 10)

# Weapon settings
MISSLE_IMG = 'thunder.png'
WAND_IMAGE_CRAFTING = 'wand.png'
MISSLE_SPEED = 1500
MISSLE_LIFETIME = 2000
MISSLE_RATE = 1000
MISSLE_DAMAGE = 30
MISSLE_KNOCKBACK = 30
MELEE_RATE = 800
WEAPON_IMG = 'sword_image.png'
WEAPON_IMG_CRAFTING = 'sword_image_crafting.png'
WEAPON_DAMAGE = 40
SWORD_KNOCKBACK = 50

RECOIL = 50
MISSLE_SPREAD = 2

# Mob settings
MOB_HEALTH = 100
MOB_DAMAGE = 15
MOB_KNOCKBACK = 20
MOB_IMG = 'troglodyte.png'
MOB_SPEED = 150
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_PLAYER_DETECTION_RANGE = 400

BOSS_HEALTH = 400
BOSS_DAMAGE = 35
BOSS_KNOCKBACK = 30
BOSS_IMG = 'minotaur.png'
BOSS_SPEED = 130
BOSS_HIT_RECT = pg.Rect(0, 0, 40, 40)

# Items
ITEM_IMAGES = {'health' : 'health_potion.png', 'magic' : 'magic_potion.png'}
HEALTH_POTION_POINTS = 50
MAGIC_POTION_POINTS = 50
PICKAXE_IMAGE = 'pickaxe.png'
AXE_IMAGE = 'axe.png'
PICKAXE_IMAGE_CRAFTING = 'pickaxe_image_crafting.png'
AXE_IMAGE_CRAFTING = 'axe_image_crafting.png'

#Obstacles
OBSTACLE_IMAGES = {'wood' : 'wood.png', 'ore' : 'ore.png'}
OBSTACLE_HIT_RECT = pg.Rect(0, 0, 30, 30)
WALL_IMG = 'wall.png'

#Sounds
SOUND_THRESHOLD = 400
BG_MUSIC_AMBIANCE = 'ambiance.mp3'
BG_MUSIC_BATTLE = 'battle.mp3'
PLAYER_SOUNDS = {'walk' :'player_walk.wav', 'attack_magic' : 'player_attack_magic.wav', 'attack_melee' : 'player_attack_melee.wav', 'death' : 'player_death.wav'}
TROGLODYTE_SOUNDS = {'walk' :'troglodyte_walk.wav', 'attack' : 'troglodyte_attack.wav', 'death' : 'troglodyte_death.wav'}
MINOTAUR_SOUNDS = {'walk' :'minotaur_walk.wav', 'attack' : 'minotaur_attack.wav', 'death' : 'minotaur_death.wav'}
POTION_SOUND = 'potion.wav'