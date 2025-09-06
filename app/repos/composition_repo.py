import pandas as pd
from app.db.sqlite import get_connection
from app.db.redis import r
import json

class CompositionRepository:
    @staticmethod
    def get_composition_by_date(date: str):
        cache_key = f"index_composition:{date}"   # 🔄 updated
        cached = r.get(cache_key)
        if cached:
            return json.loads(cached)

        conn = get_connection()
        query = """
            SELECT sm.ticker, ic.weight
            FROM index_compositions ic
            JOIN stock_metadata sm ON ic.stock_id = sm.id
            WHERE ic.date = ?
        """
        df = pd.read_sql(query, conn, params=(date,))
        conn.close()

        result = df.to_dict(orient="records") if not df.empty else []
        r.setex(cache_key, 3600, json.dumps(result))
        return result

    @staticmethod
    def get_composition_changes(start_date: str, end_date: str):
        cache_key = f"composition_changes:{start_date}:{end_date}"   # 🔄 updated
        cached = r.get(cache_key)
        if cached:
            return json.loads(cached)

        conn = get_connection()
        query = """
            SELECT ic.date, sm.ticker
            FROM index_compositions ic
            JOIN stock_metadata sm ON ic.stock_id = sm.id
            WHERE ic.date BETWEEN ? AND ?
            ORDER BY ic.date
        """
        df = pd.read_sql(query, conn, params=(start_date, end_date))
        conn.close()

        changes = []
        prev_set = set()
        for date, group in df.groupby("date"):
            current_set = set(group["ticker"])
            entered = sorted(list(current_set - prev_set))
            exited = sorted(list(prev_set - current_set))
            if entered or exited:
                changes.append({
                    "date": date,
                    "entered": entered,
                    "exited": exited
                })
            prev_set = current_set

        r.setex(cache_key, 3600, json.dumps(changes))
        return changes
