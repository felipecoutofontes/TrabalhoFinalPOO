import pygame as pg
import constants as c
import math


class Turret(pg.sprite.Sprite):
  def __init__(self, sprite_sheets, tile_x, tile_y, shot_fx, range, cooldown, damage):
    super().__init__()
    self.upgrade_level = 1
    self.range = range
    self.cooldown = cooldown
    self.damge = damage
    self.last_shot = pg.time.get_ticks()
    self.selected = False
    self.target = None

    self.tile_x = tile_x
    self.tile_y = tile_y
    #calcular coordenadas do centro
    self.x = (self.tile_x + 0.5) * c.TILE_SIZE
    self.y = (self.tile_y + 0.5) * c.TILE_SIZE
    #som dos tiros
    self.shot_fx = shot_fx

    self.sprite_sheets = sprite_sheets

    self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
    self.frame_index = 0
    self.update_time = pg.time.get_ticks()

    #update na imagem
    self.angle = 90
    self.original_image = self.animation_list[self.frame_index]
