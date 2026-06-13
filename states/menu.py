import os
import sys

import pygame

from load_data import menu_folder, menuBG, player_folder
from settings import FPS
from states.levels_menu import LevelsMenu
from utils.button import Button


class MainMenu:
    def __init__(self):
        self.levels_menu_screen = LevelsMenu()

    def draw(self):
        win = pygame.display.get_surface()
        if win is None:
            return

        screenwidth, screenheight = win.get_size()
        clock = pygame.time.Clock()

        bg_surf = pygame.transform.scale(
            pygame.image.load(os.path.join(menu_folder, "background.png")),
            (screenwidth, screenheight),
        )
        pinkey_img = pygame.image.load(
            os.path.join(player_folder, "Pink_Monster.png")
        ).convert_alpha()
        pinkey_img = pygame.transform.scale(pinkey_img, (360, 360))

        buttons = self.init_buttons(win)
        menuBG.play(-1)

        while True:
            clock.tick(FPS)
            win.blit(bg_surf, (0, 0))
            self.draw_btns(win, buttons)

            win.blit(pinkey_img, (screenwidth / 2 - (pinkey_img.get_width() / 2), 200))

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

            pygame.display.flip()

    def init_buttons(self, win):
        buttons = []
        sw = win.get_size()[0]
        sh = win.get_size()[1]
        button_bg_image = pygame.image.load(
            os.path.join(menu_folder, "ButtonBg/Default.png")
        )
        button_bg_image_hover = pygame.image.load(
            os.path.join(menu_folder, "ButtonBg/Hover.png")
        )
        play_button_icon = pygame.image.load(
            os.path.join(menu_folder, "Icons/Play.png")
        )
        back_button_icon = pygame.image.load(
            os.path.join(menu_folder, "Icons/ArrowLeft-Thin.png")
        )
        play_btn = Button(
            x=sw / 2 - 250 / 2,
            y=sh - 50 - 90 / 2,
            width=250,
            height=70,
            image=button_bg_image,
            hover_image=button_bg_image_hover,
            pressed_image=button_bg_image,
            icon=play_button_icon,
            icon_size=30,
            on_click=lambda: self.play(win),
        )
        back_btn = Button(
            x=10,
            y=10,
            width=50,
            height=50,
            image=button_bg_image,
            hover_image=button_bg_image_hover,
            pressed_image=button_bg_image,
            icon=back_button_icon,
            icon_size=30,
            on_click=lambda: pygame.quit(),
        )
        buttons.append(play_btn)
        buttons.append(back_btn)
        return buttons

    def draw_btns(self, win, buttons):
        for btn in buttons:
            btn.handle_event()
            btn.update()
            btn.draw(win)

    def play(self, win):
        self.levels_menu_screen.draw(win)
