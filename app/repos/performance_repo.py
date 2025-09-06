import pandas as pd
from app.db.sqlite import get_connection

class PerformanceRepo:
    @staticmethod
    def fetch_index_performance(start_date: str, end_date: str):
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
