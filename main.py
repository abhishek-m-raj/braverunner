import pygame

from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from states.menu import MainMenu

pygame.init()
pygame.mixer.init()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
menu = MainMenu()
menu.draw()
pygame.quit()
