import pygame as pg 

class Button:
    def __init__(self, x, y, image, single_click):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.single_click = single_click
        self.active = False  # Armazena o estado do botão

    def draw(self, surface):
        action = False
        # Obtém posição do mouse
        pos = pg.mouse.get_pos()
        
        # Verifica mouseover e condições de clique
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                # Se for single click, altera o estado
                if self.single_click:
                    self.clicked = True
                self.active = not self.active  # Alterna estado ativo
                print(f"Botão clicado! Ativo: {self.active}")
                  
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        # Desenha o botão na tela
        surface.blit(self.image, self.rect)
        
        return action
