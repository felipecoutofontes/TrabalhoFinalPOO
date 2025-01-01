import tkinter as tk
from tkinter import messagebox
import sqlite3

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

def inserir_ranking(usuario, pontos):
    conn = sqlite3.connect('ranking.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO ranking (usuario, pontos) VALUES (?, ?)
    ''', (usuario, pontos))
    conn.commit()
    conn.close()

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

def ler_dados_arquivo():
    try:
        with open('banco_dados.txt', 'r') as arquivo:
            dados = arquivo.readlines()
        return [linha.strip().split(',') for linha in dados]
    except FileNotFoundError:
        with open('banco_dados.txt', 'w'):
            pass
        return []

def verificar_login():
    global usuario_logado  
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if not usuario or not senha:
        messagebox.showerror("Erro", "Por favor, insira ambos os campos: Usuário e Senha.")
        return

    dados = ler_dados_arquivo()

    for u, s in dados:
        if u == usuario and s == senha:
            usuario_logado = usuario
            messagebox.showinfo("Login bem-sucedido", f"Bem-vindo, {usuario}!")
            return

    messagebox.showerror("Erro", "Usuário ou senha incorretos.")

def registrar_usuario():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if not usuario or not senha:
        messagebox.showerror("Erro", "Por favor, insira ambos os campos: Usuário e Senha.")
        return

    dados = ler_dados_arquivo()

    for u, s in dados:
        if u == usuario:
            messagebox.showerror("Erro", "Usuário já existe.")
            return

    try:
        with open('banco_dados.txt', 'a') as arquivo:
            arquivo.write(f"{usuario},{senha}\n")
        messagebox.showinfo("Cadastro bem-sucedido", "Usuário registrado com sucesso!")
    except IOError as e:
        messagebox.showerror("Erro", f"Erro ao registrar o usuário: {e}")

def registrar_pontuacao():
    global usuario_logado
    if usuario_logado:
        try:
            pontos = int(entry_pontuacao.get())
            inserir_ranking(usuario_logado, pontos)
            messagebox.showinfo("Pontuação registrada", f"{usuario_logado}, sua pontuação foi registrada!")
            exibir_ranking()  
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira uma pontuação válida.")
    else:
        messagebox.showerror("Erro", "Você precisa estar logado para registrar a pontuação.")

def criar_tela_login():
    global entry_usuario, entry_senha, entry_pontuacao, usuario_logado
    usuario_logado = None  

    root = tk.Tk()
    root.title("Página de Login")

    tk.Label(root, text="Usuário:").grid(row=0, column=0, padx=10, pady=10)
    entry_usuario = tk.Entry(root)
    entry_usuario.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Senha:").grid(row=1, column=0, padx=10, pady=10)
    entry_senha = tk.Entry(root, show="*")
    entry_senha.grid(row=1, column=1, padx=10, pady=10)

    botao_login = tk.Button(root, text="Login", command=verificar_login)
    botao_login.grid(row=2, column=0, columnspan=2, pady=10)

    botao_registrar = tk.Button(root, text="Registrar", command=registrar_usuario)
    botao_registrar.grid(row=3, column=0, columnspan=2, pady=10)

    tk.Label(root, text="Pontuação:").grid(row=4, column=0, padx=10, pady=10)
    entry_pontuacao = tk.Entry(root)
    entry_pontuacao.grid(row=4, column=1, padx=10, pady=10)

    botao_pontuacao = tk.Button(root, text="Registrar Pontuação", command=registrar_pontuacao)
    botao_pontuacao.grid(row=5, column=0, columnspan=2, pady=10)

    root.mainloop()

criar_banco()

criar_tela_login()
