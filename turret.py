import pygame as pg
import constants as c

class Turret(pg.sprite.Sprite):
    def __init__(self, image, pos):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos