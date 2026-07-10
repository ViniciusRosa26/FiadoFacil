from util.database.connection import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS cliente(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    apelido TEXT,
    data_criacao TEXT NOT NULL,
    saldo_devedor REAL NOT NULL DEFAULT 0.0
)
""")

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
