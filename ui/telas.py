import pygame as pg
import sys
import constants as c
from abc import ABC, abstractmethod

# Função para desenhar texto
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


# Classe abstrata para telas
class Screen(ABC):
    def __init__(self, screen):
        self.screen = screen

    @abstractmethod
    def handle_events(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass
