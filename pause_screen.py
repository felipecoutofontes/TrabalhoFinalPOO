import pygame as pg
import sys
import constants as c
from telas import Screen

# Função para desenhar texto
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Função para ajustar dinamicamente o tamanho do texto ao espaço disponível
def get_scaled_font(text, font, max_width):
    text_obj = font.render(text, True, (0, 0, 0))
    while text_obj.get_width() > max_width:
        font = pg.font.Font(font.get_name(), font.size - 1)
        text_obj = font.render(text, True, (0, 0, 0))
    return font

# Função para desenhar botões de controle de volume
def create_volume_button(text, x, y, width, height, color, font, surface, action=None):
    rect = pg.Rect(x, y, width, height)
    pg.draw.rect(surface, color, rect, border_radius=10)
    draw_text(text, font, (255, 255, 255), surface, x + width // 2, y + height // 2)
    return rect

class tela_de_pause(Screen):
    def __init__(self, screen, resume_callback, world, text_font, heart_image, coin_image):
        super().__init__(screen)
        self.resume_callback = resume_callback
        self.world = world
        self.text_font = text_font
        self.heart_image = heart_image
        self.coin_image = coin_image

        # Inicializa a fonte usada no título "Pause"
        self.font = pg.font.Font(None, 70)

        # Configurações de cores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 255)

        # Botão de continuar
        self.resume_button_text = "Continuar"
        self.resume_button_width = 200
        self.resume_button_height = 50
        self.resume_button_rect = pg.Rect(
            (c.LARGURA_TOTAL // 2 - self.resume_button_width // 2, c.SCREEN_HEIGHT // 2),
            (self.resume_button_width, self.resume_button_height),
        )

        # Botões de volume
        self.volume_buttons = [
            {"rect": None, "text": "0%", "action": lambda: pg.mixer.music.set_volume(0.0)},
            {"rect": None, "text": "50%", "action": lambda: pg.mixer.music.set_volume(0.5)},
            {"rect": None, "text": "100%", "action": lambda: pg.mixer.music.set_volume(1.0)},
        ]

        # Posição inicial dos botões
        self.button_width = 100
        self.button_height = 40
        self.button_gap = 20  # Espaço entre os botões
        self.button_y = self.resume_button_rect.bottom + 50  # Posição vertical dos botões



    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.resume_button_rect.collidepoint(event.pos):
                    self.resume_callback()
                x = (c.LARGURA_TOTAL - (len(self.volume_buttons) * self.button_width + (len(self.volume_buttons) - 1) * self.button_gap)) // 2
                for button in self.volume_buttons:
                    button_rect = pg.Rect(x, self.button_y, self.button_width, self.button_height)
                    if button_rect.collidepoint(event.pos):
                        button["action"]()
                    x += self.button_width + self.button_gap


        
    def update(self):
        pass


    def draw(self):
        # Preenche o fundo da tela
        self.screen.fill(self.WHITE)
        pg.draw.rect(self.screen, "midnightblue", (0, 0, c.LARGURA_TOTAL, c.SCREEN_HEIGHT))

        # Desenha o título
        draw_text("Pause", self.font, self.BLACK, self.screen, c.LARGURA_TOTAL // 2, c.SCREEN_HEIGHT // 4)

        # Botões de volume
        x = (c.LARGURA_TOTAL - (len(self.volume_buttons) * self.button_width + (len(self.volume_buttons) - 1) * self.button_gap)) // 2
        for button in self.volume_buttons:
            button["rect"] = create_volume_button(
                button["text"], x, self.button_y, self.button_width, self.button_height, self.BLUE, self.text_font, self.screen
            )
            x += self.button_width + self.button_gap

        # Botão de continuar
        pg.draw.rect(self.screen, self.BLUE, self.resume_button_rect)
        scaled_font = get_scaled_font(self.resume_button_text, self.text_font, self.resume_button_rect.width)
        text_surface = scaled_font.render(self.resume_button_text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=self.resume_button_rect.center)
        self.screen.blit(text_surface, text_rect.topleft)

        pg.display.flip()

   
