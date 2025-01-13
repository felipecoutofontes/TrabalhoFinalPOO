import pygame as pg
import sys
import constants as c
from telas import Screen

# Função para desenhar texto
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Tela do menu principal
class main_menu(Screen):
    def __init__(self, screen, game_loop):
        super().__init__(screen)
        self.game_loop = game_loop
        self.running = True  # Adicionar um controle de execução para o menu
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 255)
        self.font = pg.font.Font(None, 74)
        self.button_font = pg.font.Font(None, 50)
        self.button_rect = pg.Rect(c.LARGURA_TOTAL // 2 - 100, c.SCREEN_HEIGHT // 2, 200, 50)
        self.button_text = "Jogar"

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    self.running = False  # Interromper o loop do menu para iniciar o jogo

    def run(self):
        while self.running:  # Mantém o menu rodando enquanto ativo
            self.handle_events()
            self.update()
            self.draw()

    def update(self):
        pass

    def draw(self):
        self.screen.fill(self.WHITE)
        draw_text("Tower Defense", self.font, self.BLACK, self.screen, c.LARGURA_TOTAL // 2, c.SCREEN_HEIGHT // 4)
        pg.draw.rect(self.screen, self.BLUE, self.button_rect)
        draw_text(self.button_text, self.button_font, self.WHITE, self.screen, c.LARGURA_TOTAL // 2, c.SCREEN_HEIGHT // 2 + 25)
        pg.display.flip()
