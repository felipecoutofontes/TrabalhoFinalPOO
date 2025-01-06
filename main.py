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
pg.display.set_caption("Tower Defense")

#variaveis de jogo
last_enemy_spawn = pg.time.get_ticks()
placing_turrets = False
select_turret = None
selected_turret = None


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
turret_spritesheets = []
for x in range(1, c.TURRET_LEVELS + 1):
    turret_sheet = pg.image.load(f'coisas/images/turrets/turret_{x}.png').convert_alpha()
    turret_spritesheets.append(turret_sheet)
cursor_turret = pg.image.load('coisas/images/turrets/cursor_turret.png').convert_alpha()

#imagens enemies
enemy_images = {
    "weak" : load_and_scale_image('coisas/images/enemies/enemy_1.png'),
    "medium" : load_and_scale_image('coisas/images/enemies/enemy_2.png'),
    "strong" : load_and_scale_image('coisas/images/enemies/enemy_3.png'),
    "boss" : load_and_scale_image('coisas/images/enemies/enemy_4.png')
}

#botoes
buy_turret_image = pg.image.load('coisas/images/botoes/buy_turret.png').convert_alpha()
cancel_image = pg.image.load('coisas/images/botoes/cancel.png').convert_alpha()
upgrade_turret_image = pg.image.load('coisas/images/botoes/upgrade_turret.png').convert_alpha()

# Carregar o JSON do mapa
with open('levels/level.tmj') as file:
    world_data = json.load(file)

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
            new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y)
            turret_group.add(new_turret)


def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret

def clear_selection():
    for turret in turret_group:
        turret.selected = False

# Criar o mundo
world = World(world_data, map_image)
world.process_data()
world.process_enemies()

# Criar grupos
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

#cria botao
turret_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_image, True)
upgrade_button = Button(c.SCREEN_WIDTH + 5, 180, upgrade_turret_image, True)

# Loop do jogo
def game_loop():
    global placing_turrets, selected_turret, last_enemy_spawn #declarara variaveis globais
    run = True
    while run:
        clock.tick(c.FPS)
        screen.fill("grey100")
        # Atualiza
        enemy_group.update()
        turret_group.update(enemy_group)

        # Highlight da torre selecionada
        if selected_turret:
            selected_turret.selected = True

        # Desenha
        world.draw(screen)
        enemy_group.draw(screen)
        for turret in turret_group:
            turret.draw(screen)
        
        #spawn enemies
        if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
            if world.spawned_enemies < len(world.enemy_list):
                enemy_type = world.enemy_list[world.spawned_enemies]
                enemy = Enemy(enemy_type, world.waypoints, enemy_images)
                enemy_group.add(enemy)
                world.spawned_enemies += 1
                last_enemy_spawn = pg.time.get_ticks()

        if turret_button.draw(screen):
            placing_turrets = True
        
        if placing_turrets:
            cursor_rect = cursor_turret.get_rect()
            cursor_pos = pg.mouse.get_pos()
            cursor_rect.center = cursor_pos
            if cursor_pos[0] <= c.SCREEN_WIDTH:
                screen.blit(cursor_turret, cursor_rect)
            if cancel_button.draw(screen):
                placing_turrets = False
        
        #botão de upgrade aparece se um turret for selecionado
        if selected_turret:
           if selected_turret.upgrade_level < c.TURRET_LEVELS:
            if upgrade_button.draw(screen):
               selected_turret.upgrade()
        
        # Gerenciador de eventos
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                    #limpar seleção de turret
                    selected_turret = None
                    clear_selection()
                    if placing_turrets == True:
                        create_turret(mouse_pos)
                    else:
                        selected_turret = select_turret(mouse_pos)
        
        pg.display.flip()


# Executar o menu principal
main_menu(screen, game_loop)

pg.quit()

