import tkinter as tk
from tkinter import messagebox

def verificar_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    with open('banco_dados.txt', 'r') as arquivo:
        dados = arquivo.readlines()

    for linha in dados:
        u, s = linha.strip().split(',')
        if u == usuario and s == senha:
            messagebox.showinfo("Login bem-sucedido", f"Bem-vindo, {usuario}!")
            return

    messagebox.showerror("Erro", "Usuário ou senha incorretos.")

def registrar_usuario():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    with open('banco_dados.txt', 'r') as arquivo:
        dados = arquivo.readlines()

    for linha in dados:
        u, s = linha.strip().split(',')
        if u == usuario:
            messagebox.showerror("Erro", "Usuário já existe.")
            return

    with open('banco_dados.txt', 'a') as arquivo:
        arquivo.write(f"{usuario},{senha}\n")

    messagebox.showinfo("Cadastro bem-sucedido", "Usuário registrado com sucesso!")

def criar_tela_login():
    global entry_usuario, entry_senha

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

    root.mainloop()

try:
    with open('banco_dados.txt', 'r'):
        pass
except FileNotFoundError:
    with open('banco_dados.txt', 'w'):
        pass

criar_tela_login()
