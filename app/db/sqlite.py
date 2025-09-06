import sqlite3
import os
from app.config import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    """
    Initialize database by running schema.sql
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_path, "r") as f:
        conn.executescript(f.read())
    conn.close()
