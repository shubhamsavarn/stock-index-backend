import io
import time
import pandas as pd
import requests
import yfinance as yf
import sqlite3
from datetime import datetime, timedelta

DB_PATH = "db/stocks.db"

# --- Patch session headers (important for Yahoo Finance API reliability) ---
try:
    yf.shared._requests.session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    })
except Exception:
    pass


def fetch_sp500():
    """
    Fetch current S&P 500 constituents from Wikipedia.
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    df = pd.read_html(io.StringIO(response.text), attrs={"id": "constituents"})[0]

    # Fix ticker symbols that don't match Yahoo Finance format
    replacements = {"BRK.B": "BRK-B", "BF.B": "BF-A"}
    df["Symbol"] = df["Symbol"].replace(replacements)

    return df.set_index("Symbol")


def ingest_sp500(days: int = 40):
    """
    Ingest daily OHLC + Market Cap for all S&P 500 tickers into SQLite.
    """
    sp500 = fetch_sp500()
    tickers = sp500.index.tolist()

    end = datetime.today() + timedelta(days=1)  # ensures today's data is included
    start = end - timedelta(days=days)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for ticker in tickers:
        try:
            print(f"📈 Fetching {ticker} from {start.date()} to {end.date()}")
            df = yf.download(ticker, start=start, end=end, progress=False)

            if df.empty:
                print(f"⚠️ No data for {ticker}")
                continue

            # fetch shares outstanding (static)
            try:
                shares_outstanding = yf.Ticker(ticker).info.get("sharesOutstanding")
            except Exception:
                shares_outstanding = None

            df["Date"] = df.index

            # compute market cap
            if shares_outstanding:
                df["MarketCap"] = df["Close"] * shares_outstanding
            else:
                df["MarketCap"] = None

            # write into DB
            for _, row in df.iterrows():
                cur.execute(
                    """
                    INSERT OR REPLACE INTO daily_stock_prices
                    (ticker, date, open_price, high_price, low_price, close_price, volume, market_cap)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        ticker,
                        str(row["Date"].date()),
                        float(row["Open"]) if not pd.isna(row["Open"]) else None,
                        float(row["High"]) if not pd.isna(row["High"]) else None,
                        float(row["Low"]) if not pd.isna(row["Low"]) else None,
                        float(row["Close"]) if not pd.isna(row["Close"]) else None,
                        int(row["Volume"]) if not pd.isna(row["Volume"]) else None,
                        float(row["MarketCap"]) if row["MarketCap"] else None,
                    ),
                )

            conn.commit()
            time.sleep(0.5)  # avoid hitting Yahoo rate limits

        except Exception as e:
            print(f"❌ Error fetching {ticker}: {e}")

    conn.close()
    print("✅ Ingestion complete!")


if __name__ == "__main__":
    ingest_sp500(days=40)
