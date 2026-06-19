import random

import pygame

from load_data import mushroom_walkanimation_list
from systems import engine


class Mushroom:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.vel_x = random.choice([-2, 2])
        self.vel_y = 0
        self.animation = engine.Animation(mushroom_walkanimation_list, 6)
        self.flip = self.vel_x < 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, obstacles):
        # Apply gravity
        self.vel_y += 0.5
        if self.vel_y > 10:
            self.vel_y = 10

        self.y += self.vel_y
        self.rect.y = self.y

        # Ground/Wall collision
        for obs in obstacles:
            if self.rect.colliderect(obs):
                if self.vel_y > 0:
                    self.rect.bottom = obs.top
                    self.y = self.rect.y
                    self.vel_y = 0
                elif self.vel_y < 0:
                    self.rect.top = obs.bottom
                    self.y = self.rect.y
                    self.vel_y = 0

        self.x += self.vel_x
        self.rect.x = self.x

        # Wall collision (horizontal)
        hit_wall = False
        for obs in obstacles:
            if self.rect.colliderect(obs):
                if self.vel_x > 0:
                    self.rect.right = obs.left
                else:
                    self.rect.left = obs.right
                self.x = self.rect.x
                hit_wall = True
                break

        if hit_wall:
            self.vel_x *= -1
            self.flip = self.vel_x < 0
        else:
            # Ledge detection: check if there's ground ahead
            check_x = self.x + (self.width if self.vel_x > 0 else -10)
            check_rect = pygame.Rect(check_x, self.y + self.height + 2, 10, 10)
            has_ground_ahead = False
            for obs in obstacles:
                if check_rect.colliderect(obs):
                    has_ground_ahead = True
                    break

            if not has_ground_ahead:
                self.vel_x *= -1
                self.flip = self.vel_x < 0

        self.animation.update()

    def draw(self, win, scroll):
        self.animation.draw(
            win, self.x - scroll[0], self.y - scroll[1], self.flip, False
        )
