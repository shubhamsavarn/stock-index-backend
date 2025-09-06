import sqlite3
from app.providers.yfinance_provider import fetch_sp500
from app.config import DB_PATH

def ingest_metadata():
    try:
        sp500 = fetch_sp500()
        tickers = sp500.index.tolist()
    except Exception as e:
        print(f"[ERROR] Failed to fetch S&P 500 tickers: {e}")
        return

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            for ticker in tickers:
                cur.execute("""
                    INSERT OR IGNORE INTO stock_metadata (ticker) VALUES (?);
                """, (ticker,))
            conn.commit()
        print(f"[INFO] Successfully stored {len(tickers)} tickers into stock_metadata.")
    except Exception as e:
        print(f"[ERROR] Database operation failed: {e}")

def main():
    print("[INFO] Storing S&P 500 tickers into stock_metadata...")
    ingest_metadata()
    print("[INFO] Done! ✅")

if __name__ == "__main__":
    main()
