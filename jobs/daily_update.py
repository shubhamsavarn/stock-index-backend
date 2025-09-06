# daily_update.py
import sqlite3
import pandas as pd
from app.config import DB_PATH

def get_ticker_ids():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, ticker FROM stock_metadata;")
    ticker_id_map = {ticker: id for id, ticker in cur.fetchall()}
    conn.close()
    print(f"[DEBUG] Fetched ticker IDs: {ticker_id_map}")
    return ticker_id_map

def update_daily_data():
    print("[INFO] Starting daily update...")

    # Fetch ticker IDs
    ticker_id_map = get_ticker_ids()
    tickers = list(ticker_id_map.keys())

    print(f"[DEBUG] Tickers to process: {tickers}")

    # Generate sample data for the last 40 days (replace with real data fetch)
    today = pd.Timestamp.now().normalize()
    start_date = today - pd.Timedelta(days=39)

    data = {
        "ticker": sum([[ticker] * 40 for ticker in tickers], []),
        "Date": pd.date_range(end=today, periods=40).tolist() * len(tickers),
        "Open": [170.0 + i for i in range(40)] * len(tickers),
        "High": [172.0 + i for i in range(40)] * len(tickers),
        "Low": [169.0 + i for i in range(40)] * len(tickers),
        "Close": [171.0 + i for i in range(40)] * len(tickers),
        "Volume": [1000000 + i*1000 for i in range(40)] * len(tickers),
        "market_cap": [2.5e12 + i*1e10 for i in range(40)] * len(tickers),
    }
    df = pd.DataFrame(data)

    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for ticker in tickers:
        stock_id = ticker_id_map[ticker]
        ticker_df = df[df['ticker'] == ticker]
        recent_data = ticker_df[(ticker_df['Date'] >= start_date) & (ticker_df['Date'] <= today)]
        print(f"[DEBUG] Processing ticker '{ticker}': {len(recent_data)} rows")
        for _, row in recent_data.iterrows():
            date_obj = pd.to_datetime(row['Date']).date()
            print(f"[DEBUG] Inserting data for {ticker} on {date_obj}")
            cur.execute("""
                INSERT OR IGNORE INTO daily_stock_prices (
                    stock_id, date, open_price, high_price, low_price, close_price, volume, market_cap
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                stock_id,
                date_obj,
                row['Open'],
                row['High'],
                row['Low'],
                row['Close'],
                row['Volume'],
                row['market_cap']
            ))

        # Delete data older than 40 days
        delete_date = start_date - pd.Timedelta(days=1)
        print(f"[DEBUG] Deleting data older than {delete_date.date()}")
        cur.execute("""
            DELETE FROM daily_stock_prices WHERE date < ?
        """, (delete_date.date(),))
    
    conn.commit()
    conn.close()
    print("[INFO] Daily update complete.")

if __name__ == "__main__":
    update_daily_data()