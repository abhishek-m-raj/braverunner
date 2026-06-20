import os

import pygame

pygame.init()

# Base Folders
game_folder = os.path.dirname(__file__)
assets_folder = os.path.join(game_folder, "assets")

# Sub Folders
maps_folder = os.path.join(assets_folder, "maps")
font_folder = os.path.join(assets_folder, "fonts")
audio_folder = os.path.join(assets_folder, "audio")
sprites_folder = os.path.join(assets_folder, "sprites")
tiles_folder = os.path.join(assets_folder, "tiles")
ui_folder = os.path.join(assets_folder, "ui")
music_folder = os.path.join(audio_folder, "music")
sfx_folder = os.path.join(audio_folder, "sfx")
player_folder = os.path.join(sprites_folder, "player")
enemy_folder = os.path.join(sprites_folder, "enemy")
items_folder = os.path.join(sprites_folder, "items")
coin_folder = os.path.join(items_folder, "coin")
chest_folder = os.path.join(items_folder, "chest")
mushroom_folder = os.path.join(enemy_folder, "mushroom")
hud_folder = os.path.join(ui_folder, "hud")
menu_folder = os.path.join(ui_folder, "menu")

# Audio Loading
menuBG = pygame.mixer.Sound(os.path.join(music_folder, "he is a pirate.wav"))
coin_sound = pygame.mixer.Sound(os.path.join(sfx_folder, "coin.wav"))
spalsh_sound1 = pygame.mixer.Sound(os.path.join(sfx_folder, "splash1.wav"))
spalsh_sound2 = pygame.mixer.Sound(os.path.join(sfx_folder, "splash2.wav"))
jumpland = pygame.mixer.Sound(os.path.join(sfx_folder, "jumpland.wav"))

coin_animation_list = [
    pygame.image.load(os.path.join(coin_folder, f"coin{i}.png")) for i in range(1, 9)
]

walk_animation_list = [
    pygame.image.load(os.path.join(player_folder, f"walk_{i}.png")) for i in range(6)
]

idle_animation_list = [
    pygame.image.load(os.path.join(player_folder, f"idle{i}.png")) for i in range(1, 5)
]

death_animation_list = [
    pygame.image.load(os.path.join(player_folder, f"death_{i}.png")) for i in range(8)
]

mushroom_walkanimation_list = [
    pygame.image.load(os.path.join(mushroom_folder, f"mushroom_walk{i}.png"))
    for i in range(8)
]

chest_openAnimation_list = [
    pygame.image.load(os.path.join(chest_folder, f"chest_open{i}.png"))
    for i in range(1, 3)
]

coin_img = pygame.image.load(os.path.join(coin_folder, "coin1.png"))
# pinkey_img = pygame.image.load(os.path.join(player_folder, 'Pink_Monster.png')).convert()

levels = {
    "classic": {
        os.path.join(
            maps_folder,
            "classic" + "simple" + "1" + ".tmx",
        ),
        os.path.join(
            maps_folder,
            "classic" + "simple" + "2" + ".tmx",
        ),
    },
    "desert": {
        os.path.join(
            maps_folder,
            "desert" + "simple" + "1" + ".tmx",
        )
    },
}
