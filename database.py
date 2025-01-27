import sqlite3

def connect_db():
    # Conectar ao banco de dados SQLite (ou criar um novo caso não exista).
    conn = sqlite3.connect("game_data.db")
    return conn

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Criação das tabelas, caso não existam
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS scores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        score INTEGER)''')

    # Criar a tabela progress, mas verificar se as colunas health e coin já existem
    cursor.execute('''CREATE TABLE IF NOT EXISTS progress (
                        username TEXT UNIQUE,
                        level INTEGER,
                        score INTEGER,
                        health INTEGER DEFAULT 100,  -- Definindo um valor padrão
                        coin INTEGER DEFAULT 250,     -- Definindo um valor padrão
                        FOREIGN KEY (username) REFERENCES users(username))''')

    conn.commit()
    conn.close()

def create_user(username, password):
    # Criar um novo usuário no banco de dados.
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Erro: Nome de usuário já existe.")
    finally:
        conn.close()

def authenticate_user(username, password):
    # Autenticar um usuário existente.
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def save_score(username, score):
    # Salvar a pontuação de um jogador no banco de dados.
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scores (username, score) VALUES (?, ?)", (username, score))
    conn.commit()
    conn.close()
    
def get_rankings():
    # Recuperar as pontuações mais altas do banco de dados.
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username, score FROM scores ORDER BY score DESC LIMIT 10")
    rankings = cursor.fetchall()
    conn.close()
    return rankings

def save_progress(username, level, score, health, coin):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT OR REPLACE INTO progress (username, level, score, health, coin)
                      VALUES (?, ?, ?, ?, ?)''', (username, level, score, health, coin))
    conn.commit()
    conn.close()

def get_progress(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT level, score, health, coin FROM progress WHERE username=?", (username,))
    progress = cursor.fetchone()
    conn.close()
    return progress if progress else (1, 0, 100, 250)  # Se não houver progresso, começa do nível 1, saúde 100 e moedas 250

# Inicializar o banco de dados
create_tables()
