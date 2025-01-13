import pygame as pg
import sys
from database import get_rankings
from telas import Screen  # Certifique-se de que a classe base exista e tenha os métodos necessários

# Função auxiliar para desenhar texto
def draw_text(surface, text, font, color, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

class RankingScreen(Screen):  # Aqui herda de Screen (classe base)
    def __init__(self, screen):
        super().__init__(screen)  # Inicializa a classe base com a tela
        self.font = pg.font.SysFont("Arial", 36)  # Fonte maior para o título
        self.small_font = pg.font.SysFont("Arial", 24)  # Fonte menor para os rankings

    def draw(self):
        """Desenha a tela do ranking"""
        self.screen.fill((255, 255, 255))  # Limpa a tela com fundo branco
        draw_text(self.screen, "Ranking", self.font, (0, 0, 0), self.screen.get_width() // 2, 50)

        # Obtém as pontuações mais altas
        rankings = get_rankings()
        for idx, (username, score) in enumerate(rankings, 1):
            draw_text(self.screen, f"{idx}. {username} - {score}", self.small_font, (0, 0, 0),
                      self.screen.get_width() // 2, 100 + (30 * idx))

        draw_text(self.screen, "Clique com o botão direito para voltar", self.small_font, (0, 0, 0),
                  self.screen.get_width() // 2, self.screen.get_height() - 50)

    def handle_events(self):
        """Lida com os eventos da tela do ranking"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            # Verificar clique do mouse para voltar
            if event.type == pg.MOUSEBUTTONDOWN:
                return True  # Usuário clicou, retorna True para fechar ou voltar

            # Verificar pressionamento de tecla
            if event.type == pg.KEYDOWN:
                return True  # Usuário pressionou uma tecla, retorna True para fechar ou voltar

        return False  # Se nenhum evento for detectado, retorna False

    def update(self):
        """Método de atualização. No caso do ranking, não há uma atualização contínua, então pode ser vazio."""
        pass  # Ou, se necessário, adicione alguma lógica de atualização aqui.

    def run(self):
        """Executa a tela do ranking"""
        self.draw()  # Desenha a tela de ranking
        if self.handle_events():  # Verifica os eventos
            return True  # Retorna True para indicar que o ranking terminou ou foi fechado
        self.update()  # Chama o método update (agora implementado)
        pg.display.update()  # Atualiza a tela
        return False  # Retorna False para continuar na tela de ranking
