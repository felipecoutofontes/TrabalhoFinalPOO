import tkinter as tk
from tkinter import messagebox
import sqlite3

class Usuario:
    def __init__(self):
        self.__usuario_logado = None

    def set_usuario_logado(self, usuario):
        self.__usuario_logado = usuario

    def get_usuario_logado(self):
        return self.__usuario_logado

    def verificar_login(self, entry_usuario, entry_senha):
        usuario = entry_usuario.get()
        senha = entry_senha.get()

        if not usuario or not senha:
            messagebox.showerror("Erro", "Por favor, insira ambos os campos: Usuário e Senha.")
            return

        dados = self.ler_dados_arquivo()

        for u, s in dados:
            if u == usuario and self.__verificar_senha(s, senha):  # Senha privada
                self.set_usuario_logado(usuario)
                messagebox.showinfo("Login bem-sucedido", f"Bem-vindo, {usuario}!")
                return

        messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def registrar_usuario(self, entry_usuario, entry_senha):
        usuario = entry_usuario.get()
        senha = entry_senha.get()

        if not usuario or not senha:
            messagebox.showerror("Erro", "Por favor, insira ambos os campos: Usuário e Senha.")
            return

        dados = self.ler_dados_arquivo()

        for u, s in dados:
            if u == usuario:
                messagebox.showerror("Erro", "Usuário já existe.")
                return

        try:
            with open('banco_dados.txt', 'a') as arquivo:
                arquivo.write(f"{usuario},{self.__criptografar_senha(senha)}\n")  # Senha criptografada
            messagebox.showinfo("Cadastro bem-sucedido", "Usuário registrado com sucesso!")
        except IOError as e:
            messagebox.showerror("Erro", f"Erro ao registrar o usuário: {e}")

    def __verificar_senha(self, senha_armazenada, senha_digitada):
        # Compara a senha invertida com a senha digitada invertida
        return senha_armazenada == self.__criptografar_senha(senha_digitada)

    def __criptografar_senha(self, senha):
        # Simples criptografia (inversão da senha como exemplo)
        return senha[::-1]  # Inverte a senha como exemplo de criptografia

    def ler_dados_arquivo(self):
        try:
            with open('banco_dados.txt', 'r') as arquivo:
                dados = arquivo.readlines()
            return [linha.strip().split(',') for linha in dados]
        except FileNotFoundError:
            with open('banco_dados.txt', 'w'):
                pass
            return []

class Ranking:
    @staticmethod
    def criar_banco():
        conn = sqlite3.connect('ranking.db')
        c = conn.cursor()
        c.execute(''' 
            CREATE TABLE IF NOT EXISTS ranking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                pontos INTEGER NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def inserir_ranking(usuario, pontos):
        conn = sqlite3.connect('ranking.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO ranking (usuario, pontos) VALUES (?, ?)
        ''', (usuario, pontos))
        conn.commit()
        conn.close()

    @staticmethod
    def exibir_ranking():
        conn = sqlite3.connect('ranking.db')
        c = conn.cursor()
        c.execute('''
            SELECT usuario, pontos FROM ranking ORDER BY pontos DESC LIMIT 10
        ''')
        ranking = c.fetchall()
        conn.close()

        print("Ranking Top 10:")
        for i, (usuario, pontos) in enumerate(ranking, 1):
            print(f"{i}. {usuario} - {pontos} pontos")


class App:
    def __init__(self):
        self.usuario = Usuario()
        self.root = tk.Tk()
        self.root.title("Página de Login")
        self.entry_usuario = None
        self.entry_senha = None
        self.entry_pontuacao = None
        self.criar_tela_login()

    def criar_tela_login(self):
        tk.Label(self.root, text="Usuário:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_usuario = tk.Entry(self.root)
        self.entry_usuario.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Senha:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_senha = tk.Entry(self.root, show="*")
        self.entry_senha.grid(row=1, column=1, padx=10, pady=10)

        botao_login = tk.Button(self.root, text="Login", command=self.verificar_login)
        botao_login.grid(row=2, column=0, columnspan=2, pady=10)

        botao_registrar = tk.Button(self.root, text="Registrar", command=self.registrar_usuario)
        botao_registrar.grid(row=3, column=0, columnspan=2, pady=10)

        tk.Label(self.root, text="Pontuação:").grid(row=4, column=0, padx=10, pady=10)
        self.entry_pontuacao = tk.Entry(self.root)
        self.entry_pontuacao.grid(row=4, column=1, padx=10, pady=10)

        botao_pontuacao = tk.Button(self.root, text="Registrar Pontuação", command=self.registrar_pontuacao)
        botao_pontuacao.grid(row=5, column=0, columnspan=2, pady=10)

        self.root.mainloop()

    def verificar_login(self):
        self.usuario.verificar_login(self.entry_usuario, self.entry_senha)

    def registrar_usuario(self):
        self.usuario.registrar_usuario(self.entry_usuario, self.entry_senha)

    def registrar_pontuacao(self):
        usuario_logado = self.usuario.get_usuario_logado()
        if usuario_logado:
            try:
                pontos = int(self.entry_pontuacao.get())
                Ranking.inserir_ranking(usuario_logado, pontos)
                messagebox.showinfo("Pontuação registrada", f"{usuario_logado}, sua pontuação foi registrada!")
                Ranking.exibir_ranking()
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira uma pontuação válida.")
        else:
            messagebox.showerror("Erro", "Você precisa estar logado para registrar a pontuação.")

if __name__ == "__main__":
    Ranking.criar_banco()
    app = App()
