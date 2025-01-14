import pygame as pg
import sys
import constants as c
from telas import Screen
import sqlite3

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

# Função para desenhar botões
def create_button(text, x, y, width, height, color, font, surface, action=None):
    rect = pg.Rect(x, y, width, height)
    pg.draw.rect(surface, color, rect, border_radius=10)
    draw_text(text, font, (255, 255, 255), surface, x + width // 2, y + height // 2)
    return rect

# Função para conectar ao banco de dados
def connect_db():
    conn = sqlite3.connect("game_data.db")
    return conn

# Função para autenticar o usuário
def authenticate_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Função para criar um novo usuário
def create_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Erro: Nome de usuário já existe.")
    finally:
        conn.close()

class TelaDeLogin(Screen):
    def __init__(self, screen, login_callback, text_font):
        super().__init__(screen)
        self.login_callback = login_callback
        self.text_font = text_font

        # Configurações de cores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 255)

        # Tamanho dos campos de entrada e botão
        self.input_width = 300
        self.input_height = 40
        self.button_width = 200
        self.button_height = 50

        # Posições
        self.input_x = (c.LARGURA_TOTAL - self.input_width) // 2
        self.input_y = c.SCREEN_HEIGHT // 3
        self.button_x = (c.LARGURA_TOTAL - self.button_width) // 2
        self.button_y = self.input_y + 2 * self.input_height + 20

        # Inicializa os campos de texto
        self.username = ""
        self.password = ""
        self.active_input = None  # Nenhum campo ativo por padrão
        self.message = ""  # Mensagem de erro/sucesso

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            # Lida com a digitação de texto
            if event.type == pg.KEYDOWN:
                if self.active_input == "username":
                    if event.key == pg.K_BACKSPACE:
                        self.username = self.username[:-1]
                    else:
                        self.username += event.unicode
                elif self.active_input == "password":
                    if event.key == pg.K_BACKSPACE:
                        self.password = self.password[:-1]
                    else:
                        self.password += event.unicode

            # Lida com o clique nos campos de entrada e botão
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                # Verifica se clicou nos campos de texto
                username_rect = pg.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
                password_rect = pg.Rect(self.input_x, self.input_y + self.input_height + 10, self.input_width, self.input_height)
                login_button_rect = pg.Rect(self.button_x, self.button_y, self.button_width, self.button_height)
                create_account_button_rect = pg.Rect(self.button_x, self.button_y + 70, self.button_width, self.button_height)

                if username_rect.collidepoint(event.pos):
                    self.active_input = "username"
                elif password_rect.collidepoint(event.pos):
                    self.active_input = "password"
                elif login_button_rect.collidepoint(event.pos):
                    # Verificar login
                    user = authenticate_user(self.username, self.password)
                    if user:
                        self.message = "Login bem-sucedido!"
                        self.login_callback(self.username)  # Chama o callback com o nome de usuário
                    else:
                        self.message = "Erro: Usuário ou senha incorretos."
                elif create_account_button_rect.collidepoint(event.pos):
                    # Criar novo usuário
                    create_user(self.username, self.password)
                    self.message = "Conta criada com sucesso!"

                # Caso contrário, desativa qualquer campo ativo
                if not username_rect.collidepoint(event.pos) and not password_rect.collidepoint(event.pos):
                    self.active_input = None

    def update(self):
        pass

    def draw(self):
        # Preenche o fundo da tela
        self.screen.fill(self.WHITE)
        pg.draw.rect(self.screen, "midnightblue", (0, 0, c.LARGURA_TOTAL, c.SCREEN_HEIGHT))

        # Desenha o título
        draw_text("Tela de Login", self.text_font, self.WHITE, self.screen, c.LARGURA_TOTAL // 2, c.SCREEN_HEIGHT // 4)

        # Desenha os campos de texto
        username_rect = pg.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        password_rect = pg.Rect(self.input_x, self.input_y + self.input_height + 10, self.input_width, self.input_height)

        pg.draw.rect(self.screen, self.BLUE, username_rect, 2)
        pg.draw.rect(self.screen, self.BLUE, password_rect, 2)

        # Desenha o texto dentro dos campos
        draw_text(self.username, self.text_font, self.WHITE, self.screen, self.input_x + self.input_width // 2, self.input_y + self.input_height // 2)

        # Exibe a senha como asteriscos
        password_display = '*' * len(self.password)
        draw_text(password_display, self.text_font, self.WHITE, self.screen, self.input_x + self.input_width // 2, self.input_y + self.input_height + self.input_height // 2 + 10)

        # Desenha o botão de login
        create_button("Login", self.button_x, self.button_y, self.button_width, self.button_height, self.BLUE, self.text_font, self.screen)

        # Desenha o botão de criar conta
        create_button("Criar Conta", self.button_x, self.button_y + 70, self.button_width, self.button_height, self.BLUE, self.text_font, self.screen)

        # Exibe a mensagem de erro ou sucesso
        draw_text(self.message, self.text_font, self.WHITE, self.screen, c.LARGURA_TOTAL // 2, self.button_y + 150)

        pg.display.flip()
