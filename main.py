import pygame as pg
import constants as c
import sys
from enemy import Enemy


#inicia o pg
pg.init()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Fonte
font = pg.font.Font(None, 74)
button_font = pg.font.Font(None, 50)

# Funções
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def main_menu():
    while True:
        screen.fill(WHITE)

        # Desenha o título
        draw_text("Tower Defense - Oz", font, BLACK, screen, c.SCREEN_WIDTH // 2, c.SCREEN_HEIGHT // 4)

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
                    game_loop()  # Chama a função do jogo ao clicar no botão

        pg.display.flip()

#cria clock
clock = pg.time.Clock()

#cria janela do jogo
screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defense - Oz")

#redimensionar imagens
def load_and_scale_image(path, size=(83, 100)):
    image = pg.image.load(path).convert_alpha()
    return pg.transform.scale(image, size)

# Carregar a imagem redimensionada
enemy_image = load_and_scale_image('coisas\\images\\enemies\\macacoteste.png')


#criar grupos
enemy_group = pg.sprite.Group()

waypoints = [
    (100, 100),
    (400, 200),
    (400, 100),
    (200, 300)
]

enemy = Enemy(waypoints, enemy_image)
enemy_group.add(enemy)

#loop do jogo
def game_loop():
    run = True
    while run:
    
        clock.tick(c.FPS)
    
        screen.fill("grey100")
        
        #desenha caminho
        pg.draw.lines(screen, "grey0", False, waypoints)
        
        #atualizar grupos
        enemy_group.update()

        #desenha grupos
        enemy_group.draw(screen)
        
        #gerenciador de eventos
        for event in pg.event.get():
            #fecha programa
            if event.type == pg.QUIT:
                run = False
                
        #atualiza display
        pg.display.flip()    
        
main_menu()
                
pg.quit()