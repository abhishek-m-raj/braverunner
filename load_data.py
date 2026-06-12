import os

import pygame

pygame.init()
vec = pygame.math.Vector2

true_scroll = [0, 0]
vel = vec(10, 10)
paused = False
walkcount = 0

coltolerance = 10
coin_collected = 0
onGround = False
onWater = False
won = False

game_folder = os.path.dirname(__file__)
items_folder = os.path.join(game_folder, "items")
# tile_folder = os.path.join(game_folder, 'tile')
map_folder = os.path.join(game_folder, "maps")
font_folder = os.path.join(game_folder, "fonts")
sprite_folder = os.path.join(game_folder, "sprite")
enemy_folder = os.path.join(game_folder, "enemy")
hud_folder = os.path.join(game_folder, "hud")
gui_folder = os.path.join(game_folder, "GUI")
sounds_folder = os.path.join(game_folder, "sounds")

coin_folder = os.path.join(items_folder, "coin")

menuBG = pygame.mixer.Sound(os.path.join(sounds_folder, "background music.wav"))
coin_sound = pygame.mixer.Sound(os.path.join(sounds_folder, "coin.wav"))
spalsh_sound1 = pygame.mixer.Sound(os.path.join(sounds_folder, "splash1.wav"))
spalsh_sound2 = pygame.mixer.Sound(os.path.join(sounds_folder, "splash2.wav"))
jumpland = pygame.mixer.Sound(os.path.join(sounds_folder, "jumpland.wav"))

obstacle = []
coins = []
waters = []
items = []
water_hitbox = []
mushrooms = []

coin_animation_list = [
    pygame.image.load(os.path.join(coin_folder, "coin1.png")),
    pygame.image.load(os.path.join(coin_folder, "coin2.png")),
    pygame.image.load(os.path.join(coin_folder, "coin3.png")),
    pygame.image.load(os.path.join(coin_folder, "coin4.png")),
    pygame.image.load(os.path.join(coin_folder, "coin5.png")),
    pygame.image.load(os.path.join(coin_folder, "coin6.png")),
    pygame.image.load(os.path.join(coin_folder, "coin7.png")),
    pygame.image.load(os.path.join(coin_folder, "coin8.png")),
]
walk_animation_list = [
    pygame.image.load(os.path.join(sprite_folder, "walk_0.png")),
    pygame.image.load(os.path.join(sprite_folder, "walk_1.png")),
    pygame.image.load(os.path.join(sprite_folder, "walk_2.png")),
    pygame.image.load(os.path.join(sprite_folder, "walk_3.png")),
    pygame.image.load(os.path.join(sprite_folder, "walk_4.png")),
    pygame.image.load(os.path.join(sprite_folder, "walk_5.png")),
]
idle_animation_list = [
    pygame.image.load(os.path.join(sprite_folder, "idle1.png")),
    pygame.image.load(os.path.join(sprite_folder, "idle2.png")),
    pygame.image.load(os.path.join(sprite_folder, "idle3.png")),
    pygame.image.load(os.path.join(sprite_folder, "idle4.png")),
]
death_animation_list = [
    pygame.image.load(os.path.join(sprite_folder, "death_0.png")),
    pygame.image.load(os.path.join(sprite_folder, "death_1.png")),
    pygame.image.load(os.path.join(sprite_folder, "death_2.png")),
    pygame.image.load(os.path.join(sprite_folder, "death_3.png")),
    pygame.image.load(os.path.join(sprite_folder, "death_4.png")),
    pygame.image.load(os.path.join(sprite_folder, "death_5.png")),
    pygame.image.load(os.path.join(sprite_folder, "death_6.png")),
    pygame.image.load(os.path.join(sprite_folder, "death_7.png")),
]
mushroom_walkanimation_list = [
    pygame.image.load(os.path.join(enemy_folder, "mushroom_walk0.png")),
    pygame.image.load(os.path.join(enemy_folder, "mushroom_walk1.png")),
    pygame.image.load(os.path.join(enemy_folder, "mushroom_walk2.png")),
    pygame.image.load(os.path.join(enemy_folder, "mushroom_walk3.png")),
    pygame.image.load(os.path.join(enemy_folder, "mushroom_walk4.png")),
    pygame.image.load(os.path.join(enemy_folder, "mushroom_walk5.png")),
    pygame.image.load(os.path.join(enemy_folder, "mushroom_walk6.png")),
    pygame.image.load(os.path.join(enemy_folder, "mushroom_walk7.png")),
]
chest_openAnimation_list = [
    pygame.image.load(os.path.join(items_folder, "chest_open1.png")),
    pygame.image.load(os.path.join(items_folder, "chest_open2.png")),
]

# hud images for menus and games
coin_img = pygame.image.load(os.path.join(coin_folder, "coin1.png"))
# pinkey_img = pygame.image.load(os.path.join(sprite_folder, 'Pink_Monster.png')).convert()

uparrow_img = pygame.image.load(os.path.join(gui_folder, "uparrow.png"))
rightarrow_img = pygame.image.load(os.path.join(gui_folder, "rightarrow.png"))
leftarrow_img = pygame.image.load(os.path.join(gui_folder, "leftarrow.png"))
