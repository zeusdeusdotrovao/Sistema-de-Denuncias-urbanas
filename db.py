"""
app/db.py — Conexão com o banco de dados SQLite.
"""

import sqlite3

BANCO = "database.db"


def get_db():
    """Retorna uma conexão com o banco. Cada linha vira um dicionário."""
    conn = sqlite3.connect(BANCO)
    conn.row_factory = sqlite3.Row  # permite acessar colunas pelo nome
    return conn
