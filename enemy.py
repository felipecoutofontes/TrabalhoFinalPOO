import pygame as pg
from pygame.math import Vector2
import math
import constants as c
from enemy_data import ENEMY_DATA


class Enemy(pg.sprite.Sprite):
  def __init__(self, enemy_type, waypoints, images):
    super().__init__()
    self.waypoints = waypoints
    self.pos = Vector2(self.waypoints[0])
    self.target_waypoint = 1
    self.health = ENEMY_DATA.get(enemy_type)["health"]
    self.speed = ENEMY_DATA.get(enemy_type)["speed"]
    self.damage = ENEMY_DATA.get(enemy_type)["damage"]
    self.original_speed = self.speed
    self.angle = 0
    self.original_image = images.get(enemy_type)
    self.image = pg.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = self.pos

  def update(self, world, enemy_type):
    self.move(world)
    self.rotate()
    self.check_alive(world, enemy_type)

  def move(self, world):
    #define waypoint alvo
    if self.target_waypoint < len(self.waypoints):
      self.target = Vector2(self.waypoints[self.target_waypoint])
      self.movement = self.target - self.pos
    else:
      #enemy chegou no fim do caminho
      self.kill()
      world.health -= self.damage
      world.missed_enemies += 1

    #calcula distancia ate o alvo
    dist = self.movement.length()
    #checa se distancia remanescente é maior que a velocidade de enemy
    if dist >= (self.speed * world.game_speed) :
      self.pos += self.movement.normalize() * (self.speed * world.game_speed)
    else: 
      if dist != 0:
        self.pos += self.movement.normalize() * dist
      self.target_waypoint += 1



  def rotate(self):
    #calcula distancia ate o proximo waypoint
    dist = self.target - self.pos
    #usa distancia para calcular angulo
    self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
    #rotaciona imagem e atualiza retangulo
    self.image = pg.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = self.pos
  
  def check_alive(self, world, enemy_type):
    if self.health <= 0:
      world.killed_enemies += 1
      world.money += ENEMY_DATA.get(enemy_type)["kill_reward"]
      self.kill()