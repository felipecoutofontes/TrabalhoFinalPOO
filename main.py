import pygame as pg
import json
import constants as c
from enemy import Enemy
from world import World
from turret import Turret
from button import Button
from interface import main_menu

# Inicia o pygame
pg.init()

# Cria o clock
clock = pg.time.Clock()

# Configura a janela do jogo
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defense - Oz")

# Funções auxiliares para carregar imagens
def load_and_scale_image(path, size=(81, 100)):
    image = pg.image.load(path).convert_alpha()
    return pg.transform.scale(image, size)

def load_and_scale_image1(path, size=(54, 67)):
    image = pg.image.load(path).convert_alpha()
    return pg.transform.scale(image, size)

def load_and_scale_image2(path, size=(c.SCREEN_WIDTH, c.SCREEN_HEIGHT)):
    image = pg.image.load(path).convert_alpha()
    return pg.transform.scale(image, size)

# Carregar imagens
map_image = load_and_scale_image2('coisas/images/fases/level.png')
cursor_turret = load_and_scale_image1('coisas/images/turrets/macacoteste1.png')
enemy_image = load_and_scale_image('coisas/images/enemies/macacoteste.png')
#botoes
buy_turret_image = pg.image.load('coisas/images/botoes/buy_turret.png').convert_alpha()
cancel_image = pg.image.load('coisas/images/botoes/cancel.png').convert_alpha()



# Carregar o JSON do mapa
with open('levels/level.tmj') as file:
    world_data = json.load(file)

# Criar o mundo
world = World(world_data, map_image)
world.process_data()

# Criar grupos
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

#cria botao
turret_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image)
cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_image)


if world.waypoints:
    enemy = Enemy(world.waypoints, enemy_image)
enemy_group.add(enemy)

# Função para criar uma torre
def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x

    if world.tile_map[mouse_tile_num] == 7:  # Verifica se o tile é válido
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False
        if space_is_free:
            new_turret = Turret(cursor_turret, mouse_tile_x, mouse_tile_y)
            turret_group.add(new_turret)

# Loop do jogo
def game_loop():
    run = True
    while run:
        clock.tick(c.FPS)
        screen.fill("grey100")
        # Atualiza
        enemy_group.update()



        # Desenha
        world.draw(screen)
        enemy_group.draw(screen)
        turret_group.draw(screen)
        
        
        if turret_button.draw(screen):
            print("new turret")
            
            
        if cancel_button.draw(screen):
            print("cancel")
        
        
        

        # Gerenciador de eventos
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                    create_turret(mouse_pos)

        pg.display.flip()

# Executar o menu principal
main_menu(screen, game_loop)

pg.quit()
