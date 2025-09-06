# db/database.py

import sqlite3
from contextlib import contextmanager
from typing import Optional, Any, List, Tuple

# Path to your SQLite DB file
DB_PATH = "db/stock_data.sqlite"


@contextmanager
def get_db_conn():
    """
    Context manager for SQLite connection.
    Ensures connection is always closed.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # allows dict-like row access
    try:
        yield conn
    finally:
        conn.close()


def fetch_all(query: str, params: Optional[Tuple[Any, ...]] = None) -> List[sqlite3.Row]:
    """
    Run SELECT and return all rows.
    """
    with get_db_conn() as conn:
        cur = conn.cursor()
        cur.execute(query, params or [])
        return cur.fetchall()


def fetch_one(query: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[sqlite3.Row]:
    """
    Run SELECT and return a single row.
    """
    with get_db_conn() as conn:
        cur = conn.cursor()
        cur.execute(query, params or [])
        return cur.fetchone()


def execute_query(query: str, params: Optional[Tuple[Any, ...]] = None) -> None:
    """
    Run INSERT, UPDATE, or DELETE.
    Commits automatically.
    """
    with get_db_conn() as conn:
        cur = conn.cursor()
        cur.execute(query, params or [])
        conn.commit()
