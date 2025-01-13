import pygame as pg
import math
from abc import ABC, abstractmethod
import constants as c
from enemy_data import ENEMY_DATA
from enemy import Enemy

class Turret(pg.sprite.Sprite, ABC):
    def __init__(self, sprite_sheet, tile_x, tile_y, range, cooldown, damage):
        super().__init__()
        self.range = range
        self.cooldown = cooldown
        self.damage = damage
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.target = None
        

        self.tile_x = tile_x
        self.tile_y = tile_y
        #calcular coordenadas do centro
        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE
        #som dos tiros

        self.sprite_sheet = sprite_sheet
        self.animation_list = self.load_images(self.sprite_sheet)
        self.frame_index =0
        self.update_time = pg.time.get_ticks()

        #update de imagem
        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        

        # Circulo para mostrar range
        self.range_image = pg.Surface((self.range * 2, self.range * 2), pg.SRCALPHA)
        pg.draw.circle(self.range_image, (255, 255, 255, 100), (self.range, self.range), self.range)
        self.range_rect = self.range_image.get_rect(center=(self.x, self.y))

    def load_images(self, sprite_sheet):
        #extrai imagens da spritesheet
        size = sprite_sheet.get_height()
        animation_list = []
        for x in range(c.ANIMATION_STEPS):
            temp_img = sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def draw(self, surface):
        rotated_image = pg.transform.rotate(self.original_image, self.angle - 90)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        surface.blit(rotated_image, rotated_rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
        

    def play_animation(self):
            #update imagem
            self.original_image = self.animation_list[self.frame_index]
            #checa o tempo desde o ultimo update
            if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
                self.update_time = pg.time.get_ticks()
                self.frame_index += 1
            #checa se a animaçao resetou
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                self.last_shot = pg.time.get_ticks()
                self.target = None

    @abstractmethod
    def update(self, enemy_group, world):
        pass

    @abstractmethod
    def pick_target(self, enemy_group, world):
        pass


class TurretBasica(Turret, pg.sprite.Sprite):
    def __init__(self, sprite_sheet, tile_x, tile_y):
        super().__init__(sprite_sheet, tile_x, tile_y, range=150, cooldown=1000, damage=10)

    def update(self, enemy_group, world):
        if self.target:
            self.play_animation()
        else:
            if pg.time.get_ticks() - self.last_shot > (self.cooldown/ world.game_speed):
                self.pick_target(enemy_group)

    def pick_target(self, enemy_group):
        x_dist = 0
        y_dist = 0
        for enemy in enemy_group:
            if enemy.health >= 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist**2 + y_dist**2)
                if dist < self.range:
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    #danificar o enemy
                    self.target.health -= self.damage
                break


class TurretSniper(Turret, pg.sprite.Sprite):
    def __init__(self, sprite_sheet, tile_x, tile_y):
        super().__init__(sprite_sheet, tile_x, tile_y, range=200, cooldown=2000, damage=10)

    def update(self, enemy_group, world):
        if self.target:
            self.play_animation()
        else:
            if pg.time.get_ticks() - self.last_shot > (self.cooldown/ world.game_speed):
                self.pick_target(enemy_group)

    def pick_target(self, enemy_group):
        x_dist = 0
        y_dist = 0
        for enemy in enemy_group:
            if enemy.health >= 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist**2 + y_dist**2)
                if dist < self.range:
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    #danificar o enemy
                    self.target.health -= self.damage
                break


class TurretSlow(Turret, pg.sprite.Sprite):
    def __init__(self, sprite_sheet, tile_x, tile_y):
        super().__init__(sprite_sheet, tile_x, tile_y, range=150, cooldown=600, damage=2)
        self.slow_factor = 0.5
        self.slow_duration = 120
        self.attacked_enemies ={}
        self.current_time= pg.time.get_ticks()

    def update(self, enemy_group, world):
        if self.target:
            self.play_animation()
            self.target = None
        else:
            if pg.time.get_ticks() - self.last_shot > (self.cooldown/ world.game_speed):
                self.pick_target(enemy_group)


    def pick_target(self, enemy_group):
        x_dist = 0
        y_dist = 0
        for enemy in enemy_group:
            if enemy.health>= 0 and (enemy.speed == enemy.original_speed) :
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist**2 + y_dist**2)
                if dist <= self.range:
                    self.target = enemy
                    self.last_shot = pg.time.get_ticks()
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    self.target.speed *= self.slow_factor
                    self.target.health -= self.damage
                    break


class TurretTop(Turret, pg.sprite.Sprite):
    def __init__(self, sprite_sheet, tile_x, tile_y):
        super().__init__(sprite_sheet, tile_x, tile_y, range=200, cooldown=800, damage=20)
        self.slow_factor = 0.5
        self.slow_duration = 120

    def update(self, enemy_group, world):
        if self.target:
            self.play_animation()
        else:
            if pg.time.get_ticks() - self.last_shot > (self.cooldown/ world.game_speed):
                self.pick_target(enemy_group)

    def pick_target(self, enemy_group):
        x_dist = 0
        y_dist = 0
        for enemy in enemy_group:
            if enemy.health >= 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist**2 + y_dist**2)
                if dist < self.range:
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    #danificar o enemy
                    self.target.health -= self.damage
                break
