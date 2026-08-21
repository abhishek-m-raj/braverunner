import os

import pygame

from settings import GAME_OVER_SOUND_VOLUME, MENU_MUSIC_VOLUME, WIN_SOUND_VOLUME

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

class DummySound:
    def play(self, *args, **kwargs):
        pass
    def stop(self, *args, **kwargs):
        pass
    def set_volume(self, *args, **kwargs):
        pass


def load_sound(folder, filename):
    base, ext = os.path.splitext(filename)
    candidates = [
        f"{base}-pygbag.ogg",
        f"{base}.ogg",
        f"{base}.wav",
        f"{base}.mp3",
        filename,
        f"{filename}-pygbag.ogg",
        f"{filename}.ogg",
        f"{filename}.wav",
        f"{filename}.mp3",
    ]
    for cand in candidates:
        full_path = os.path.join(folder, cand)
        if os.path.exists(full_path):
            try:
                return pygame.mixer.Sound(full_path)
            except (pygame.error, Exception) as e:
                print(f"Failed to load audio candidate {full_path}: {e}")
    print(f"Warning: Could not load sound {filename}, using dummy sound.")
    return DummySound()


# Audio Loading
menuBG = load_sound(music_folder, "he is a pirate")
menuBG.set_volume(MENU_MUSIC_VOLUME)
coin_sound = load_sound(sfx_folder, "coin")
spalsh_sound1 = load_sound(sfx_folder, "splash1")
spalsh_sound2 = load_sound(sfx_folder, "splash2")
jumpland = load_sound(sfx_folder, "jumpland")
game_over_sound = load_sound(music_folder, "game over")
game_over_sound.set_volume(GAME_OVER_SOUND_VOLUME)
win_sound = load_sound(music_folder, "win")
win_sound.set_volume(WIN_SOUND_VOLUME)

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

FONT_NAME = "ChakraPetch-Bold.ttf"
FONT_PATH = os.path.join(font_folder, FONT_NAME)

LEVELS = [
    {"id": "classic1", "path": os.path.join(maps_folder, "classic1.tmx"), "category": "classic", "name": "Classic 1"},
    {"id": "classic2", "path": os.path.join(maps_folder, "classic2.tmx"), "category": "classic", "name": "Classic 2"},
    {"id": "desert1", "path": os.path.join(maps_folder, "desert1.tmx"), "category": "desert", "name": "Desert 1"},
    {"id": "graveyard1", "path": os.path.join(maps_folder, "graveyard1.tmx"), "category": "graveyard", "name": "Graveyard 1"},
]

levels = {}
for lvl in LEVELS:
    cat = lvl["category"]
    if cat not in levels:
        levels[cat] = []
    levels[cat].append(lvl)
