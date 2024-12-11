import pygame as pg 

class Button():
    def __init__(self, x, y, image, single_click):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.single_click = single_click
        
        
    def draw(self, surface):
        action = False
        #get mouse position
        pos = pg.mouse.get_pos()
        
        #checa mouseover e condiçoes de clique
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                #se for single click set click to true
                if self.single_click:
                    self.clicked = True
                  
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        #desenha botao na tela
        surface.blit(self.image, self.rect)
        
        return action