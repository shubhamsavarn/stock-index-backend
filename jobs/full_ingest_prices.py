import sqlite3
import pandas as pd
import yfinance as yf
import datetime
from app.config import DB_PATH

def get_ticker_ids():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, ticker FROM stock_metadata;")
    ticker_id_map = {ticker: id for id, ticker in cur.fetchall()}
    conn.close()
    print(f"[DEBUG] Fetched ticker IDs: {ticker_id_map}")
    return ticker_id_map

def get_real_data(symbol: str):
    """Fetch real OHLC, Volume, and Market Cap data for the last 40 days."""
    end = datetime.date.today()
    start = end - datetime.timedelta(days=40)
    ticker = yf.Ticker(symbol)
    hist = ticker.history(start=start, end=end, interval="1d")
    
    if hist.empty:
        print(f"[WARNING] No data fetched for {symbol}")
        return pd.DataFrame()
    
    shares_outstanding = ticker.info.get("sharesOutstanding")
    hist.reset_index(inplace=True)
    hist["Date"] = hist["Date"].astype(str)

    # Round OHLC to 2 decimal places
    hist["Open"] = hist["Open"].round(2)
    hist["High"] = hist["High"].round(2)
    hist["Low"] = hist["Low"].round(2)
    hist["Close"] = hist["Close"].round(2)

    # Convert MarketCap to trillions
    if shares_outstanding:
        hist["MarketCap"] = (hist["Close"] * shares_outstanding) / 1e12
        hist["MarketCap"] = hist["MarketCap"].round(3)
    else:
        hist["MarketCap"] = None

    # Ensure Volume is integer
    hist["Volume"] = hist["Volume"].astype('Int64')

    return hist[["Date", "Open", "High", "Low", "Close", "Volume", "MarketCap"]]

def ingest_prices():
    ticker_id_map = get_ticker_ids()
    if not ticker_id_map:
        print("[ERROR] No tickers found in stock_metadata table.")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for ticker, stock_id in ticker_id_map.items():
        print(f"[INFO] Starting ingestion for {ticker}...")
        df = get_real_data(ticker)
        if df.empty:
            print(f"[WARNING] No data fetched for {ticker}. Skipping...")
            continue

        for _, row in df.iterrows():
            date_obj = pd.to_datetime(row["Date"]).date()
            print(f"[DEBUG] Inserting data for {ticker} on {date_obj}")
            print(f"  Open: {row['Open']}, High: {row['High']}, Low: {row['Low']}, Close: {row['Close']}")
            print(f"  Volume: {row['Volume']}, MarketCap (Trillions): {row['MarketCap']}")

            cur.execute("""
                INSERT OR IGNORE INTO daily_stock_prices (
                    stock_id, date, open_price, high_price, low_price, close_price, volume, market_cap
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                stock_id,
                date_obj,
                row["Open"],
                row["High"],
                row["Low"],
                row["Close"],
                row["Volume"],
                row["MarketCap"]
            ))
        conn.commit()
        print(f"[INFO] Ingestion for {ticker} complete.")

    conn.close()
    print("[INFO] Ingestion for all tickers complete.")

if __name__ == "__main__":
    ingest_prices()
