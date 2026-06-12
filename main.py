import os

import pygame
import pytmx

import engine
import load_data
from load_data import *

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

win = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
screenwidth = win.get_width()
screenheight = win.get_height()
controlsurf = pygame.Surface((screenwidth, screenheight))

coin_animation = engine.Animation(load_data.coin_animation_list, 4)
walk_animation = engine.Animation(walk_animation_list, 6)
idle_animation = engine.Animation(idle_animation_list, 8)
death_animation = engine.Animation(death_animation_list, 8)
mushroom_walkanimation = engine.Animation(mushroom_walkanimation_list, 6)
chest_openAnimation = engine.Animation(chest_openAnimation_list, 10)


class TiledMap:
    def __init__(self, filename):
        global tm
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for (
                    x,
                    y,
                    gid,
                ) in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(
                            tile,
                            (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight),
                        )

    def make_map(self):
        global temp_surface
        temp_surface = pygame.Surface((self.width, self.height)).convert()
        self.render(temp_surface)
        return temp_surface


class player:
    def __init__(self, w, h):
        self.isjump = False
        self.jumpcount = 12
        self.left = False
        self.right = False
        self.idle = False
        self.death = False
        self.width = w
        self.height = h

    def setlocation(self, x, y):
        self.x = x
        self.y = y

    def events(self, mosx, mosy):
        win.blit(controlsurf, (0, 0))
        controlsurf.set_colorkey((0, 0, 0))
        controlsurf.set_alpha(150)
        uparrow = controlsurf.blit(
            uparrow_img,
            (100, screenheight - 150),
        )
        rightarrow = controlsurf.blit(
            rightarrow_img,
            (screenwidth - 150, screenheight - 150),
        )
        leftarrow = controlsurf.blit(
            leftarrow_img,
            (screenwidth - 300, screenheight - 150),
        )

        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_LEFT] or leftarrow.collidepoint(mosx, mosy):
            self.left = True
            self.right = False
        elif self.keys[pygame.K_RIGHT] or rightarrow.collidepoint(mosx, mosy):
            self.right = True
            self.left = False
        else:
            if not (self.death):
                self.idle = True
            self.right = False
            self.left = False
            self.walkcount = 0

        if not (self.isjump):
            if (
                self.keys[pygame.K_SPACE]
                or self.keys[pygame.K_UP]
                or uparrow.collidepoint(mosx, mosy)
            ):
                self.isjump = True
                self.right = False
                self.left = False
                self.walkcount = 0
        else:
            if self.jumpcount >= -9:
                self.neg = 1
                if self.jumpcount < 0:
                    self.neg = -0.5
                self.y -= (self.jumpcount**2) * self.neg * 0.5
                self.jumpcount -= 1
            else:
                pygame.mixer.Sound.play(jumpland)
                self.isjump = False
                self.jumpcount = 12

    def draw(self):
        if self.left:
            self.x -= vel.x
            walk_animation.draw(win, self.x - scroll[0], self.y, False, 0)
        elif self.right:
            self.x += vel.x
            walk_animation.draw(win, self.x - scroll[0], self.y, True, 0)
        elif self.idle:
            idle_animation.draw(win, self.x - scroll[0], self.y, 0, 0)

        if self.death:
            self.left = False
            self.right = False
            self.idle = False
            death_animation.draw(win, self.x - scroll[0], self.y, 0, 0)
            # win.fill((0,0,0))
            # text = engine.drawText(win, "game over", screenwidth/2, screenheight/2, ((255,0,0)))

        if not (paused):
            walk_animation.update()
            death_animation.update()
            idle_animation.update()


class GUI:
    def __init__(self):
        self.place = ""
        self.difficulty = "simple"
        self.number = 1
        # self.maper = TiledMap(os.path.join(maps_folder, self.place + self.difficulty + str(self.number) + '.tmx'))
        # self.map_img = self.maper.make_map().convert()
        # self.map_rect = self.map_img.get_rect()

    def main_menu(self):
        global screenwidth, screenheight, win, controlsurf
        classic_img = pygame.transform.scale(
            pygame.image.load(os.path.join(menu_folder, "desert bt.png")), (100, 100)
        )
        deset_img = pygame.transform.scale(
            pygame.image.load(os.path.join(menu_folder, "classic bt.png")), (100, 100)
        )
        bg_surf = pygame.transform.scale(
            pygame.image.load(os.path.join(menu_folder, "background.png")),
            (screenwidth, screenheight),
        )
        pinkey_img = pygame.image.load(
            os.path.join(player_folder, "Pink_Monster.png")
        ).convert()
        scaled_pinkey = pygame.transform.scale(
            pinkey_img, (int(screenwidth / 3), int(screenheight - 400))
        )
        play_btn_img = pygame.image.load("play.png")
        back_btn_img = pygame.image.load(os.path.join(menu_folder, "back.png"))

        pygame.mixer.Sound.play(menuBG, -1)

        while True:
            clock.tick(60)
            win.blit(bg_surf, (0, 0))

            classic_rect = win.blit(classic_img, (500, 500))
            desert_rect = win.blit(deset_img, (500, 650))
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
                    import sys

                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    screenwidth, screenheight = event.size
                    win = pygame.display.set_mode(
                        (screenwidth, screenheight), pygame.RESIZABLE
                    )
                    controlsurf = pygame.Surface((screenwidth, screenheight))

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
                import sys

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
                    self.game()
            elif options_rect.collidepoint(mx, my) and clicked:
                self.options()
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

    def options(self):
        global screenwidth, screenheight, win, controlsurf
        running = True
        back_btn_img = pygame.image.load(os.path.join(menu_folder, "back.png"))
        while running:
            clock.tick(60)
            win.fill((0, 0, 0))
            back_img_rect = win.blit(back_btn_img, (50, 50))
            t = "options"
            engine.drawText(
                win, t, screenwidth / 2, screenheight / 3, ((255, 255, 255)), 54
            )

            clicked = False
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
                    controlsurf = pygame.Surface((screenwidth, screenheight))

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        clicked = True

            mx, my = pygame.mouse.get_pos()

            if back_img_rect.collidepoint(mx, my) and clicked:
                running = False

            pygame.display.flip()

    def game(self):
        global screenwidth, screenheight, win, controlsurf
        run = True
        man = player(64, 64)
        pygame.mixer.Sound.stop(menuBG)
        global onGround, coin_collected, chest_rect
        for tile_object in self.maper.tmxdata.objects:
            if tile_object.name == "player":
                playerx = tile_object.x
                playery = tile_object.y
                man.setlocation(playerx, playery)
            if tile_object.name == "coin":
                coin_data = pygame.Rect(tile_object.x, tile_object.y, 32, 32)
                coins.append(coin_data)
            elif tile_object.name == "water":
                water_start_x = tile_object.x
                water_end_x = tile_object.x + tile_object.width
                water_start_y = tile_object.y + tile_object.width
                water_end_y = tile_object.y
                water_rect = pygame.Rect(
                    (
                        tile_object.x,
                        tile_object.y,
                        tile_object.width,
                        tile_object.height,
                    )
                )
                water_hitbox.append(water_rect)
                water_metric = [
                    water_start_x,
                    water_end_x,
                    water_start_y,
                    water_end_y,
                    3,
                ]
                waters.append(water_metric)
            elif tile_object.name == "wall":
                hit_rect = pygame.Rect(
                    tile_object.x, tile_object.y, tile_object.width, tile_object.height
                )
                pygame.draw.rect(temp_surface, (255, 0, 0), hit_rect, 2)
                obstacle.append(hit_rect)
            elif tile_object.name == "mushroom":
                mushroom_x = tile_object.x
                mushroom_y = tile_object.y
                mushroom_pos = pygame.Rect(mushroom_x, mushroom_y, 16, 16)
                mushrooms.append(mushroom_pos)
            elif tile_object.name == "chest":
                chest = ["chest", tile_object.x, tile_object.y]
                chest_rect = pygame.Rect(
                    tile_object.x, tile_object.y, tile_object.width, tile_object.height
                )
                items.append(chest)

        # for water_metric in waters:
        #     # waterie = Main(int(water_metric[0]),int(water_metric[1]),temp_surface)
        #     # pygame.draw.rect(temp_surface,(0,0,0),water,water_surface,2)
        #     water_test = water(water_metric[0],water_metric[1],water_metric[2],water_metric[3],water_metric[4])
        #     temp_surface.blit(water_test.draw(temp_surface,water_test,self.map_rect.width,self.map_rect.height,alpha), (0,0))

        back_btn_img = pygame.image.load(os.path.join(menu_folder, "back.png"))
        pause_btn_img = pygame.image.load(os.path.join(menu_folder, "pause.png"))
        chest_open1_img = pygame.image.load(
            os.path.join(chest_folder, "chest_open1.png")
        )

        while run:
            clock.tick(60)
            left_border = 0
            right_border = self.map_img.get_width()
            true_scroll[0] += (man.x - true_scroll[0] - screenwidth // 4) / 20
            true_scroll[0] = max(left_border, true_scroll[0])
            true_scroll[0] = min(true_scroll[0], right_border - screenwidth)

            global scroll
            scroll = true_scroll.copy()
            scroll[0] = int(scroll[0])
            scroll[1] = int(scroll[1])

            win.blit(self.map_img, (0 - scroll[0], 0))

            alpha = 100

            acc = vec(0, 12)
            vel.y += acc.y
            man.y += vel.y

            player_hitbox = pygame.Rect((man.x + 17, man.y - 13, 28, 52))
            player_hitbox.y += vel.y
            back_img_rect = win.blit(back_btn_img, (50, 50))
            pause_img_rect = win.blit(pause_btn_img, (150, 50))

            # for w in water_hitbox:
            #     if player_hitbox.colliderect(w):
            #         if player_hitbox.y - w.y - player_hitbox.h <= coltolerance:
            #             water_test.splash(30,5)
            #             water_test.update(0.25)
            #             vel.x = vel.x/2
            #             vel.y = vel.y/2
            #             break
            #     else:
            #         vel.x = 10
            #         vel.y = 10

            # water_test.splash(50,100)
            for c in coins[:]:
                coin_animation.draw(win, c.x - scroll[0], c.y, 0, 0)
                if player_hitbox.colliderect(c):
                    pygame.mixer.Sound.play(coin_sound)
                    coins.remove(c)
                    coin_collected += 1

            for i in obstacle:
                if i.colliderect(player_hitbox):
                    if player_hitbox.x - i.x + i.w <= coltolerance:
                        man.x = i.x + i.w
                        break
                    elif player_hitbox.x - i.x - player_hitbox.w <= coltolerance:
                        man.x = i.x - player_hitbox.w
                        vel.x = 0
                        break
                    elif player_hitbox.y - i.y + i.h <= coltolerance:
                        man.y = i.y + i.h
                        break
                    elif player_hitbox.y - i.y - player_hitbox.h <= coltolerance:
                        onGround = True
                        man.y = i.y - player_hitbox.h - 10
                        vel.y = 0
                        break
                    else:
                        vel.x = 10
                        vel.y = 10
                        onGround = False

            clicked = False
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
                    controlsurf = pygame.Surface((screenwidth, screenheight))

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        clicked = True

            mx, my = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()

            if pause_img_rect.collidepoint(mx, my) and clicked:
                paused = True

            if back_img_rect.collidepoint(mx, my) and clicked:
                run = False

            # gravity
            if not (onGround):
                man.y += vel.y
            elif onGround or isjump:
                vel.y = 0

            if keys[pygame.K_ESCAPE]:
                reset = False
                run = False
                scroll[0] = 0

            # player_hitbox = pygame.Rect((man.x+17,man.y+11,28,52))
            # pygame.draw.rect(win, (0,0,0),(player_hitbox.x - scroll[0],player_hitbox.y,player_hitbox.w,player_hitbox.h),2)
            win.blit(coin_img, (screenwidth - 40, 10))
            engine.drawText(
                win,
                str(coin_collected),
                screenwidth - 55,
                1,
                ((0, 0, 0)),
                32,
                align="tl",
            )

            for mush in mushrooms:
                mushroom_walkanimation.draw(win, mush.x - scroll[0], mush.y, 0, 0)
                if player_hitbox.colliderect(mush):
                    death = True
                else:
                    death = False

            for item in items:
                if item[0] == "chest":
                    global won
                    chest_img = temp_surface.blit(
                        chest_open1_img,
                        (item[1], item[2]),
                    )
                    if player_hitbox.colliderect(chest_rect):
                        pygame.draw.rect(temp_surface, (0, 0, 0), chest_img, 3)
                        won = True
                    else:
                        won = False

            if won:
                chest_openAnimation.draw(win, chest_img.x, chest_img.y, 0, 0)
                chest_openAnimation.update()

            coin_animation.update()
            mushroom_walkanimation.update()
            chest_openAnimation.update()
            # water_test.update(0.025)
            man.draw()
            man.events(mx, my)
            pygame.display.flip()


menu = GUI()
menu.main_menu()
pygame.quit()
