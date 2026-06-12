import os
import sys
from cmath import e

import pygame

from load_data import maps_folder, menu_folder, menuBG, player_folder
from states.level import Level
from systems.tilemap import TiledMap


class MainMenu:
    def __init__(self):
        self.place = ""
        self.difficulty = "simple"
        self.number = 1
        self.maper = None
        self.map_img = None
        self.map_rect = None

    def draw(self):
        win = pygame.display.get_surface()
        if win is None:
            return

        screenwidth, screenheight = win.get_size()
        clock = pygame.time.Clock()

        desert_img = pygame.transform.scale(
            pygame.image.load(os.path.join(menu_folder, "desert bt.png")), (100, 100)
        )
        classic_img = pygame.transform.scale(
            pygame.image.load(os.path.join(menu_folder, "classic bt.png")), (100, 100)
        )

        bg_surf = pygame.transform.scale(
            pygame.image.load(os.path.join(menu_folder, "background.png")),
            (screenwidth, screenheight),
        )
        pinkey_img = pygame.image.load(
            os.path.join(player_folder, "Pink_Monster.png")
        ).convert_alpha()

        scaled_pinkey = pygame.transform.scale(
            pinkey_img, (int(screenwidth / 3), int(screenheight - 400))
        )

        play_btn_img = pygame.image.load("play.png").convert_alpha()
        back_btn_img = pygame.image.load(
            os.path.join(menu_folder, "back.png")
        ).convert_alpha()

        pygame.mixer.Sound.play(menuBG, -1)

        while True:
            clock.tick(60)
            win.blit(bg_surf, (0, 0))

            classic_rect = win.blit(classic_img, (500, 500))
            desert_rect = win.blit(desert_img, (500, 650))
            win.blit(scaled_pinkey, (screenwidth / 2 - 200, 200))
            play_img_rect = win.blit(play_btn_img, (screenwidth / 2, screenheight / 2))

            options_rect = pygame.draw.rect(
                win, (255, 0, 0), (screenwidth / 2, screenheight / 4, 300, 100)
            )
            back_img_rect = win.blit(back_btn_img, (50, 50))

            clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    screenwidth, screenheight = event.size
                    win = pygame.display.set_mode(
                        (screenwidth, screenheight), pygame.RESIZABLE
                    )

                    bg_surf = pygame.transform.scale(
                        pygame.image.load(os.path.join(menu_folder, "background.png")),
                        (screenwidth, screenheight),
                    )
                    scaled_pinkey = pygame.transform.scale(
                        pinkey_img, (int(screenwidth / 3), int(screenheight - 400))
                    )

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        clicked = True

            mx, my = pygame.mouse.get_pos()

            if back_img_rect.collidepoint(mx, my) and clicked:
                pygame.quit()
                sys.exit()
            elif desert_rect.collidepoint(mx, my) and clicked:
                if self.place != "desert":
                    self.place = "desert"
                    self.maper = TiledMap(
                        os.path.join(
                            maps_folder,
                            "desert" + self.difficulty + str(self.number) + ".tmx",
                        )
                    )
                    self.map_img = self.maper.make_map()
                    self.map_rect = self.map_img.get_rect()
            elif play_img_rect.collidepoint(mx, my) and clicked:
                if self.place != "":
                    pygame.mixer.Sound.stop(menuBG)
                    Level(self.maper).draw()
            elif classic_rect.collidepoint(mx, my) and clicked:
                if self.place != "classic":
                    self.place = "classic"
                    self.maper = TiledMap(
                        os.path.join(
                            maps_folder,
                            "classic" + self.difficulty + str(self.number) + ".tmx",
                        )
                    )
                    self.map_img = self.maper.make_map()
                    self.map_rect = self.map_img.get_rect()

            if self.place == "classic":
                pygame.draw.rect(win, (0, 0, 0), classic_rect, 3)
            elif self.place == "desert":
                pygame.draw.rect(win, (0, 0, 0), desert_rect, 3)

            pygame.display.flip()
