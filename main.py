# /// script
# dependencies = [
#   "pytmx",
#   "pygame-ce",
# ]
# ///

import asyncio
import os
import sys

import pygame
import pytmx

from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from states.level import Level
from states.levels_menu import LevelsMenu
from states.menu import MainMenu
from systems.tilemap import TiledMap


async def main():
    pygame.init()
    pygame.mixer.init()
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    menu = MainMenu()
    await menu.draw()
    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())


