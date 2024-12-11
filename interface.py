import pygame as pg
import sys
import constants as c

# Função para desenhar texto
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Função do menu principal
def main_menu(screen, game_loop):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)

    font = pg.font.Font(None, 74)
    button_font = pg.font.Font(None, 50)

    while True:
        screen.fill(WHITE)

        # Desenha o título
        draw_text("Tower Defense", font, BLACK, screen, c.SCREEN_WIDTH // 2, c.SCREEN_HEIGHT // 4)

        # Configuração do botão
        button_text = "Jogar"
        button_rect = pg.Rect(c.SCREEN_WIDTH // 2 - 100, c.SCREEN_HEIGHT // 2, 200, 50)
        pg.draw.rect(screen, BLUE, button_rect)

        # Exibe o texto do botão
        draw_text(button_text, button_font, WHITE, screen, c.SCREEN_WIDTH // 2, c.SCREEN_HEIGHT // 2 + 25)

        # Verifica eventos
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    game_loop()  # Chama o jogo ao clicar no botão

        pg.display.flip()
