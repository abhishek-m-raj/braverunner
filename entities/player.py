import pygame

import load_data
from settings import VELOCITY
from systems import engine

walk_animation = engine.Animation(load_data.walk_animation_list, 6)
idle_animation = engine.Animation(load_data.idle_animation_list, 8)
death_animation = engine.Animation(load_data.death_animation_list, 8, loop=False)


class Player:
    def __init__(self):
        self.onGround = False
        self.isjump = False
        self.jumps_made = 0
        self.jump_key_held = False
        self.left = False
        self.right = False
        self.idle = True
        self.death = False
        self.width = 64
        self.height = 64
        self.x = 0
        self.y = 0
        self.last_flip = False

    def setlocation(self, x, y):
        self.x = x
        self.y = y

    def handle_inputs(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.move_left()
        elif keys[pygame.K_RIGHT]:
            self.move_right()
        else:
            self.stop_moving()

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if not self.jump_key_held:
                self.jump()
                self.jump_key_held = True
        else:
            self.jump_key_held = False

        self.onGround = False

    def move_left(self):
        self.left = True
        self.right = False
        self.idle = False
        self.last_flip = True

    def move_right(self):
        self.right = True
        self.left = False
        self.idle = False
        self.last_flip = False

    def stop_moving(self):
        if not self.death:
            self.idle = True
        self.left = False
        self.right = False
        self.walkcount = 0

    def jump(self):
        if self.jumps_made < 2:
            pygame.mixer.Sound.play(load_data.jumpland)
            self.isjump = True
            self.onGround = False
            self.jumps_made += 1

            VELOCITY.y = -18
            self.right = False
            self.left = False
            self.walkcount = 0

    def update_position(self):
        if self.left:
            self.x -= VELOCITY.x
        elif self.right:
            self.x += VELOCITY.x

    def draw(self, win, scroll):
        screen_x = self.x - scroll[0]
        screen_y = self.y - scroll[1]

        if self.death:
            if not death_animation.finished:
                death_animation.draw(win, screen_x, screen_y, self.last_flip)
        elif self.left:
            walk_animation.draw(win, screen_x, screen_y, True)
        elif self.right:
            walk_animation.draw(win, screen_x, screen_y, False)
        elif self.idle:
            idle_animation.draw(win, screen_x, screen_y, self.last_flip)

    def reset_death(self):
        self.death = False
        death_animation.reset()

    def update_animations(self):
        if self.death:
            death_animation.update()
        elif self.idle:
            idle_animation.update()
        else:
            walk_animation.update()
