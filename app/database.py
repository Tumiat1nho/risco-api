import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "risco.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS avaliacoes_risco (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            situacao_cadastral TEXT,
            capital_social REAL,
            data_inicio_atividade TEXT,
            nivel_risco TEXT NOT NULL,
            pontuacao INTEGER NOT NULL,
            observacao TEXT,
            data_avaliacao TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()
