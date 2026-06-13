import os

import pygame

import load_data
from entities.player import Player
from load_data import coin_img, coin_sound, menu_folder
from settings import DEBUG, GRAVITY, VELOCITY
from states.overlay import GameOverlay
from systems import engine
from utils.button import Button

coin_animation = engine.Animation(load_data.coin_animation_list, 4)


class Level:
    def __init__(self, maper):
        self.maper = maper
        self.map_img = self.maper.make_map().convert()
        self.goal_rect = None
        self.coin_collected = 0
        self.coins = []
        self.obstacles = []
        self.scroll = [0.0, 0.0]
        self.pause_overlay = GameOverlay(
            "Game Paused",
            [
                {"text": "Resume", "status": "resume"},
                {"text": "Home", "status": "home"},
                {"text": "Quit", "status": "quit"},
            ],
        )
        self.win_overlay = GameOverlay(
            "Level Complete!",
            [{"text": "Home", "status": "home"}, {"text": "Quit", "status": "quit"}],
        )

    def draw(self):
        run = True
        win = pygame.display.get_surface()
        if win is None:
            return

        screenwidth, screenheight = win.get_size()
        clock = pygame.time.Clock()

        player = Player()

        for tile_object in self.maper.tmxdata.objects:
            if tile_object.name == "player":
                playerx = tile_object.x
                playery = tile_object.y
                player.setlocation(playerx, playery)
            if tile_object.name == "coin":
                coin_data = pygame.Rect(tile_object.x, tile_object.y, 32, 32)
                self.coins.append(coin_data)
            elif tile_object.name == "wall":
                hit_rect = pygame.Rect(
                    tile_object.x, tile_object.y, tile_object.width, tile_object.height
                )
                self.obstacles.append(hit_rect)
            elif tile_object.name == "goal":
                goal_rect = pygame.Rect(
                    tile_object.x, tile_object.y, tile_object.width, tile_object.height
                )
                self.goal_rect = goal_rect

        # UI Buttons
        button_bg = pygame.image.load(os.path.join(menu_folder, "ButtonBg/Default.png"))
        button_bg_hover = pygame.image.load(
            os.path.join(menu_folder, "ButtonBg/Hover.png")
        )
        icon_back = pygame.image.load(
            os.path.join(menu_folder, "Icons/ArrowLeft-Thin.png")
        )
        icon_pause = pygame.image.load(os.path.join(menu_folder, "Icons/Pause.png"))

        def on_back_click():
            nonlocal run
            run = False

        def on_pause_click():
            status = self.pause_overlay.draw(win)
            if status == "home":
                nonlocal run
                run = False
            elif status == "quit":
                pygame.quit()
                import sys

                sys.exit()

        back_btn = Button(
            50,
            50,
            60,
            60,
            on_back_click,
            image=button_bg,
            hover_image=button_bg_hover,
            icon=icon_back,
            icon_size=30,
        )
        pause_btn = Button(
            130,
            50,
            60,
            60,
            on_pause_click,
            image=button_bg,
            hover_image=button_bg_hover,
            icon=icon_pause,
            icon_size=30,
        )

        while run:
            clock.tick(60)

            self.camera_update(player, win, screenwidth, screenheight)

            player.handle_inputs()

            player.update_position()
            player_hitbox = pygame.Rect(player.x + 22, player.y + 22, 20, 42)
            for obstacle in self.obstacles:
                if player_hitbox.colliderect(obstacle):
                    if player.right:
                        player.x = obstacle.left - 22 - 20
                    elif player.left:
                        player.x = obstacle.right - 22
                    player_hitbox.x = player.x + 22

            VELOCITY.y += GRAVITY.y * 0.1
            if VELOCITY.y > 15:
                VELOCITY.y = 15
            player.y += VELOCITY.y

            if self.goal_rect and player_hitbox.colliderect(self.goal_rect):
                status = self.win_overlay.draw(win)
                if status == "home":
                    run = False
                elif status == "quit":
                    pygame.quit()
                    import sys

                    sys.exit()

            player_hitbox = pygame.Rect(player.x + 22, player.y + 22, 20, 42)
            for obstacle in self.obstacles:
                if player_hitbox.colliderect(obstacle):
                    if (
                        VELOCITY.y >= 0
                        and player_hitbox.bottom > obstacle.top
                        and player_hitbox.centery < obstacle.top
                    ):
                        player.y = obstacle.top - 42 - 22
                        player.onGround = True
                        player.jumps_made = 0
                        VELOCITY.y = 0
                        player.isjump = False
                    elif (
                        VELOCITY.y < 0
                        and player_hitbox.top < obstacle.bottom
                        and player_hitbox.centery > obstacle.bottom
                    ):
                        player.y = obstacle.bottom - 22
                        VELOCITY.y = 0
                        player.isjump = False
                    player_hitbox.y = player.y + 22  # Keep hitbox in sync

            if DEBUG:
                self.draw_debug_hitboxes(win, player)

            back_btn.handle_event()
            back_btn.update()
            back_btn.draw(win)

            pause_btn.handle_event()
            pause_btn.update()
            pause_btn.draw(win)

            self.draw_coins(win, player_hitbox)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    import sys

                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    screenwidth, screenheight = event.size
                    win = pygame.display.set_mode(
                        (screenwidth, screenheight), pygame.RESIZABLE
                    )
                    back_btn.set_location(50, 50)
                    pause_btn.set_location(130, 50)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                on_pause_click()

            win.blit(coin_img, (screenwidth - 40, 10))
            engine.drawText(
                win,
                str(self.coin_collected),
                screenwidth - 55,
                1,
                ((0, 0, 0)),
                32,
                align="tl",
            )

            coin_animation.update()
            player.update_animations()
            player.draw(win, self.scroll)
            pygame.display.flip()

    def camera_update(self, player, win, screenwidth, screenheight):
        left_border = 0
        right_border = self.map_img.get_width()
        top_border = 0
        bottom_border = self.map_img.get_height()

        self.scroll[0] += (player.x - self.scroll[0] - screenwidth // 4) / 20
        self.scroll[0] = max(left_border, self.scroll[0])
        self.scroll[0] = min(self.scroll[0], right_border - screenwidth)

        self.scroll[1] += (player.y - self.scroll[1] - screenheight // 2) / 20
        self.scroll[1] = max(top_border, self.scroll[1])
        self.scroll[1] = min(self.scroll[1], bottom_border - screenheight)

        self.scroll[0] = int(self.scroll[0])
        self.scroll[1] = int(self.scroll[1])

        win.blit(self.map_img, (0 - self.scroll[0], 0 - self.scroll[1]))

    def draw_coins(self, win, player_hitbox):
        for c in self.coins:
            coin_animation.draw(win, c.x - self.scroll[0], c.y - self.scroll[1])
            if player_hitbox.colliderect(c):
                pygame.mixer.Sound.play(coin_sound)
                self.coins.remove(c)
                self.coin_collected += 1

    def draw_debug_hitboxes(self, win, player):
        for obs in self.obstacles:
            pygame.draw.rect(
                win,
                (255, 0, 0),
                (obs.x - self.scroll[0], obs.y - self.scroll[1], obs.w, obs.h),
                2,
            )
        pygame.draw.rect(
            win,
            (0, 255, 0),
            (player.x + 22 - self.scroll[0], player.y + 22 - self.scroll[1], 20, 42),
            2,
        )
