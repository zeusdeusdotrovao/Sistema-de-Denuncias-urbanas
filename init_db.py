"""
init_db.py — Inicializa o banco de dados SQLite.
Execute uma vez antes de rodar o servidor: python init_db.py
"""

import sqlite3

BANCO = "database.db"

def criar_tabelas():
    conn = sqlite3.connect(BANCO)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS denuncias (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            endereco         TEXT    NOT NULL,
            cep              TEXT,
            ponto_referencia TEXT,
            tipo             TEXT    NOT NULL,
            descricao        TEXT,
            status           TEXT    NOT NULL DEFAULT 'aberta',
            latitude         REAL,
            longitude        REAL,
            data             DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("Banco de dados criado com sucesso!")

if __name__ == "__main__":
    criar_tabelas()
