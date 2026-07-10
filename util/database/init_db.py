from database.connection import get_connection #se conectnado a classe connection

conn = get_connection()

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS cliente(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    apelido TEXT,
    data_criacao TEXT NOT NUUL
)
""")
 # cursor eh qm faz os comandos sql
cursor.execute("""  
CREATE TABLE IF NOT EXISTS movimentacao(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    descricao TEXT,
    valor REAL NOT NULL,
    tipo TEXT NOT NULL,
    data_hora TEXT NOT NULL,

    FOREIGN KEY(cliente_id) REFERENCES cliente(id)
)
""")

conn.commit()
conn.close()