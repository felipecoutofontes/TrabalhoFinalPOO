import pygame as pg
import json
import constants as c
from enemy import Enemy
from world import World
from turret import Turret
from button import Button
from menu import main_menu
from pause_screen import tela_de_pause


# Inicia o pygame
pg.init()


# Configura a música de fundo
pg.mixer.music.load('coisas/sons/musica.mp3')  # Caminho para o arquivo de música
pg.mixer.music.set_volume(0.5)  # Define o volume inicial (ajustável)
pg.mixer.music.play(-1)  # Toca a música em loop (-1 indica repetição infinita)

# Cria o clock
clock = pg.time.Clock()

# Configura a janela do jogo
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defense")

#variaveis de jogo
game_over = False
game_outcome = 0 #-1 perdeu e 1 ganhou
level_started = False
last_enemy_spawn = pg.time.get_ticks()
placing_turrets = False
select_turret = None
selected_turret = None



# Funções auxiliares para carregar imagens
def load_and_scale_image(path, size=(81, 100)):
    image = pg.image.load(path).convert_alpha()
    return pg.transform.scale(image, size)

def load_and_scale_image1(path, size=(35, 35)):
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
    "weak" : pg.image.load('coisas/images/enemies/enemy_1.png').convert_alpha(),
    "medium" : pg.image.load('coisas/images/enemies/enemy_2.png').convert_alpha(),
    "strong" : pg.image.load('coisas/images/enemies/enemy_3.png').convert_alpha(),
    "boss" : pg.image.load('coisas/images/enemies/enemy_4.png').convert_alpha()
}

#botoes
buy_turret_image = pg.image.load('coisas/images/botoes/buy_turret.png').convert_alpha()
cancel_image = pg.image.load('coisas/images/botoes/cancel.png').convert_alpha()
upgrade_turret_image = pg.image.load('coisas/images/botoes/upgrade_turret.png').convert_alpha()
begin_image = pg.image.load('coisas/images/botoes/begin.png').convert_alpha()
restart_image = pg.image.load('coisas/images/botoes/restart.png').convert_alpha()
fast_foward_image = pg.image.load('coisas/images/botoes/fast_foward.png').convert_alpha()
pause_button_image = load_and_scale_image1('coisas/images/botoes/pause.png')


#gui
heart_image = pg.image.load('coisas/images/interface/heart.png').convert_alpha()
coin_image = pg.image.load('coisas/images/interface/coin.png').convert_alpha()

#sons
shot_fx = pg.mixer.Sound('coisas/sons/shot.wav')
shot_fx.set_volume(0.5)

# Carregar o JSON do mapa
with open('levels/level.tmj') as file:
    world_data = json.load(file)

#carregar fontes de display
text_font = pg.font.SysFont("Consolas", 24, bold = True)
large_font = pg.font.SysFont("Consolas", 36)

#função pra saida de txto na tela
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def display_data():
    #desenha painel
    pg.draw.rect(screen, "midnightblue", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, c.SCREEN_HEIGHT ))
    #pg.draw.rect(screen, "white", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, 400 ), 4)
    #screen.blit(logo_image, (c.SCREEN_WIDTH, 400))
    #display informações
    pg.draw.rect(screen, "steelblue4", (c.SCREEN_WIDTH + 70, 16, 170, 40 ), border_radius = 30)
    draw_text("NÍVEL: " + str(world.level), text_font, "grey100", c.SCREEN_WIDTH + 100, 22) 
    screen.blit(heart_image, (c.SCREEN_WIDTH + 115, 60))
    draw_text(str(world.health), text_font, "grey100", c.SCREEN_WIDTH + 155, 65) 
    screen.blit(coin_image, (c.SCREEN_WIDTH + 115, 90))
    draw_text(str(world.money), text_font, "grey100", c.SCREEN_WIDTH + 155, 95 ) 
    #draw_text("Para fazer upgrades, selecione a torre que deseja alterar.", text_font, "grey100", c.SCREEN_WIDTH + 20, 600)

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
            new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y, shot_fx)
            turret_group.add(new_turret)
            #SUBTRAIR CUSTO DE TURRET
            world.money -= c.BUY_COST


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
turret_button = Button(c.SCREEN_WIDTH + 30, 150, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 60, 150, cancel_image, True)
upgrade_button = Button(c.SCREEN_WIDTH + 5, 180, upgrade_turret_image, True)
begin_button = Button(c.SCREEN_WIDTH + 70, 300, begin_image, True)
restart_button = Button(310, 300, restart_image, True)
fast_foward_button = Button(c.SCREEN_WIDTH + 60, 450, fast_foward_image, single_click=True) # se for true o botao é só de um clique mas o false vc segura
pause_button = Button(c.SCREEN_WIDTH + 30, 10, pause_button_image, single_click=True)


fast_forward_active = False
world.game_speed = 1
paused = False #variável para o estado de pausa
show_begin_button = True


def resume_game():
    global paused
    paused = False

def initialize_game():
    global placing_turrets, selected_turret, last_enemy_spawn, level_started, game_over, world, game_outcome, paused, show_begin_button

    
    placing_turrets = False
    selected_turret = None
    last_enemy_spawn = pg.time.get_ticks()
    level_started = False
    game_over = False
    paused = False
    game_outcome = 0  # Nenhum resultado
    world = World(world_data, map_image)
    world.process_data()
    world.process_enemies()
    enemy_group.empty()
    turret_group.empty()


# Loop do jogo
def game_loop():
    global placing_turrets, selected_turret, last_enemy_spawn, level_started, game_over, world, game_outcome, fast_forward_active, paused, show_begin_button

    
    run = True
    while run:
        clock.tick(c.FPS)

 
        
        # Verificar se o jogo acabou
        if not game_over:
            if world.health <= 0:
                game_over = True
                game_outcome = -1  # perdeu
            elif world.level > c.TOTAL_LEVELS:
                game_over = True
                game_outcome = 1  # ganhou

            # Atualizações durante o jogo
            if not paused:
                # Atualizar inimigos e torres
                enemy_group.update(world)
                turret_group.update(enemy_group, world)
                
            # Highlight da torre selecionada
            if selected_turret:
                selected_turret.selected = True    

            # Spawn de inimigos
            if level_started == False:
                if begin_button.draw(screen):
                    level_started = True
            else:
                #acelerar os inimigos
                if fast_foward_button.active:
                    world.game_speed = 3
                else:
                    world.game_speed = 1    
                if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
                    if world.spawned_enemies < len(world.enemy_list):
                        enemy_type = world.enemy_list[world.spawned_enemies]
                        enemy = Enemy(enemy_type, world.waypoints, enemy_images)
                        enemy_group.add(enemy)
                        world.spawned_enemies += 1
                        last_enemy_spawn = pg.time.get_ticks()

                #checar se a onda de enemies acabou
                if world.check_level_complete() == True:
                    world.money += c.LEVEL_COMPLETE_REWARD
                    world.level += 1
                    level_started = False
                    last_enemy_spawn = pg.time.get_ticks()
                    world.reset_level()
                    world.process_enemies()
                    
                    
        # Desenho da tela
        world.draw(screen)
        enemy_group.draw(screen)
        for turret in turret_group:
            turret.draw(screen)

        # Exibir informações
        display_data()

        if not game_over:
            # Botão de início do nível
            if show_begin_button and begin_button.draw(screen):
                level_started = True
                show_begin_button = False  # Esconde o botão ao ser pressionado
          
        # Botão de fast forward
        if fast_foward_button.draw(screen):
            world.game_speed = 3
        

        # Botão de pausa
        if not game_over and pause_button.draw(screen):
            paused = not paused

        # Lógica de posicionamento de torres
        if not placing_turrets:
            draw_text(str(c.BUY_COST), text_font, "grey100", c.SCREEN_WIDTH + 205, 165)
            screen.blit(coin_image, (c.SCREEN_WIDTH + 250, 160))
            if turret_button.draw(screen):
                placing_turrets = True
        else:
            cursor_rect = cursor_turret.get_rect()
            cursor_pos = pg.mouse.get_pos()
            cursor_rect.center = cursor_pos
            if cursor_pos[0] <= c.SCREEN_WIDTH:
                screen.blit(cursor_turret, cursor_rect)
            if cancel_button.draw(screen):
                placing_turrets = False

        # Botão de upgrade da torre selecionada
        if selected_turret:
            if selected_turret.upgrade_level < c.TURRET_LEVELS:
                draw_text(str(c.UPGRADE_COST), text_font, "grey100", c.SCREEN_WIDTH + 217, 195)
                screen.blit(coin_image, (c.SCREEN_WIDTH + 250, 190))
                if upgrade_button.draw(screen):
                    if world.money >= c.UPGRADE_COST:
                        selected_turret.upgrade()
                        world.money -= c.UPGRADE_COST

        # Tela de pausa
        if paused and not game_over:
            pause_screen = tela_de_pause(screen, resume_game, world, text_font, heart_image, coin_image)
            pause_screen.handle_events()
            pause_screen.draw()

        # Tela de game over
        if game_over:
            pg.draw.rect(screen, "dodgerblue", (200, 200, 400, 200), border_radius=30)
            draw_text(
                "GAME OVER :(" if game_outcome == -1 else "DIVOU!",
                large_font, "grey0", 400, 300
            )
            if restart_button.draw(screen):
                initialize_game()
                game_over = False
                
        # Gerenciador de eventos
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                if not paused and not game_over:
                    if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                        clear_selection()
                        if placing_turrets and world.money >= c.BUY_COST:
                            create_turret(mouse_pos)
                        else:
                            selected_turret = select_turret(mouse_pos)

        # Atualizar a tela
        pg.display.flip()


    pg.quit()





# Inicializar o menu principal e iniciar o jogo
initialize_game()
menu = main_menu(screen, game_loop)  # Cria uma instância do menu
menu.run()  # Executa o menu até o jogador clicar em "Jogar"

# Quando o menu terminar, o jogo será iniciado
game_loop()  # Inicia o loop principal do jogo

pg.quit()  # Fecha o pygame corretamente ao final


