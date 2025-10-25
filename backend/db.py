import sqlite3

from .config import settings


def get_conn():
    conn = sqlite3.connect(settings.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(schema_path: str):
    with get_conn() as conn, open(schema_path, encoding='utf-8') as f:
        conn.executescript(f.read())
