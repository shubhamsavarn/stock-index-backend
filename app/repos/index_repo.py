from typing import List, Tuple
import pandas as pd
from app.db.sqlite import get_connection
from app.db.redis import r

class IndexRepository:

    # -------------------------------
    # Fetch stock prices for index calculation
    # -------------------------------
    @staticmethod
    def fetch_stock_prices(start_date: str, end_date: str) -> pd.DataFrame:
        conn = get_connection()
        query = """
            SELECT dsp.date, dsp.stock_id, dsp.close_price, dsp.market_cap
            FROM daily_stock_prices dsp
            WHERE dsp.date BETWEEN ? AND ?
            ORDER BY dsp.date ASC, dsp.market_cap DESC
        """
        df = pd.read_sql(query, conn, params=(start_date, end_date))
        conn.close()
        return df

    # -------------------------------
    # Save index compositions
    # -------------------------------
    @staticmethod
    def save_compositions(compositions: List[Tuple[str, int, float]]):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM index_compositions")
        cur.executemany(
            "INSERT INTO index_compositions(date, stock_id, weight) VALUES (?, ?, ?)",
            compositions
        )
        conn.commit()
        conn.close()

    # -------------------------------
    # Save index performance
    # -------------------------------
    @staticmethod
    def save_performance(perf_rows: List[Tuple[str, float, float, float]]):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM index_performance")
        cur.executemany(
            "INSERT INTO index_performance(date, index_level, daily_return, cumulative_return) VALUES (?, ?, ?, ?)",
            perf_rows
        )
        conn.commit()
        conn.close()

    # -------------------------------
    # Fetch compositions by date
    # -------------------------------
    @staticmethod
    def get_compositions(date: str) -> pd.DataFrame:
        conn = get_connection()
        query = """
            SELECT sm.ticker, ic.weight
            FROM index_compositions ic
            JOIN stock_metadata sm ON ic.stock_id = sm.id
            WHERE ic.date = ?
        """
        df = pd.read_sql(query, conn, params=(date,))
        conn.close()
        return df

    # -------------------------------
    # Fetch performance in range
    # -------------------------------
    @staticmethod
    def get_performance(start_date: str, end_date: str) -> pd.DataFrame:
        conn = get_connection()
        query = """
            SELECT date, index_level, daily_return, cumulative_return
            FROM index_performance
            WHERE date BETWEEN ? AND ?
            ORDER BY date
        """
        df = pd.read_sql(query, conn, params=(start_date, end_date))
        conn.close()
        return df

    # -------------------------------
    # Invalidate caches
    # -------------------------------
    @staticmethod
    def invalidate_cache():
        r.delete("index_comp:*")
        r.delete("index_performance:*")
        r.delete("comp_changes:*")
