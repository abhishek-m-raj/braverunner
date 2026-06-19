import os

import pygame

from load_data import font_folder


def drawText(
    screen, t, x, y, c, size, hold=False, holdside="", align="c", fonte="Mukta.ttf"
):
    fontstyle = os.path.join(font_folder, fonte)
    font = pygame.font.Font(fontstyle, size)
    text = font.render(t, True, c)
    hold_x = 0
    hold_y = 0
    screen_rectangle = screen.get_rect()
    text_rectangle = text.get_rect()
    if align == "c":
        text_rectangle.center = (x, y)
    elif align == "l":
        text_rectangle.left = (x, y)
    elif align == "r":
        text_rectangle.right = (x, y)
    elif align == "t":
        text_rectangle.top = (x, y)
    elif align == "b":
        text_rectangle.bottom = (x, y)
    elif align == "tl":
        text_rectangle.topleft = (x, y)
    elif align == "tr":
        text_rectangle.topright = (x, y)
    elif align == "bl":
        text_rectangle.bottomleft = (x, y)
    elif align == "br":
        text_rectangle.bottomright = (x, y)

    if not (hold):
        screen.blit(text, text_rectangle)
    else:
        if holdside == "top":
            screen_rectangle.top = hold_x, hold_y
            screen.blit(text, (hold_x, hold_y))
        elif holdside == "bottom":
            screen_rectangle.bottom = hold_x, hold_y
            screen.blit(text, (hold_x, hold_y))
        elif holdside == "center":
            screen_rectangle.center = hold_x, hold_y
            screen.blit(text, (hold_x, hold_y))


class Position:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)


class Animation:
    def __init__(self, imageList, animationSpeed, loop=True):
        self.imageList = imageList
        self.imageIndex = 0
        self.animationTimer = 0
        self.animationSpeed = animationSpeed
        self.loop = loop
        self.finished = False

    def update(self):
        self.animationTimer += 1
        if self.animationTimer >= self.animationSpeed:
            self.animationTimer = 0
            self.imageIndex += 1

            if self.imageIndex > len(self.imageList) - 1:
                if self.loop:
                    self.imageIndex = 0
                else:
                    self.imageIndex = len(self.imageList) - 1
                    self.finished = True
                    return  # Stop updating once finished

    def draw(self, screen, x, y, flipX=False, flipY=False):
        screen.blit(
            pygame.transform.flip(self.imageList[self.imageIndex], flipX, flipY), (x, y)
        )

    def reset(self):
        self.imageIndex = 0
        self.animationTimer = 0
        self.finished = False

    def get_current_image(self):
        return self.imageList[self.imageIndex]
