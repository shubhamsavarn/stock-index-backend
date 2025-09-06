import schedule
import time
import datetime
from jobs.daily_update import update_daily_data as daily_ingest
from jobs.full_ingest_prices import ingest_prices as full_ingest  # keep as-is if function is ingest_prices
from jobs.ingest_data import ingest_metadata

def run_daily():
    print(f"[INFO] Running daily_update.py at {datetime.datetime.now()}")
    try:
        daily_ingest()
    except Exception as e:
        print(f"[ERROR] daily_update.py failed: {e}")

def run_full_ingest():
    print(f"[INFO] Running full_ingest_prices.py at {datetime.datetime.now()}")
    try:
        full_ingest()
    except Exception as e:
        print(f"[ERROR] full_ingest_prices.py failed: {e}")

def run_ingest_data():
    print(f"[INFO] Running ingest_data.py at {datetime.datetime.now()}")
    try:
        ingest_metadata()
    except Exception as e:
        print(f"[ERROR] ingest_data.py failed: {e}")

# Schedule daily_update.py at 2:00 AM
schedule.every().day.at("02:00").do(run_daily)

# Schedule monthly jobs at 3:00 AM on 1st day
def monthly_jobs():
    if datetime.datetime.now().day == 1:
        run_full_ingest()
        run_ingest_data()

schedule.every().day.at("03:00").do(monthly_jobs)

print("[INFO] Scheduler started. Press Ctrl+C to exit.")

while True:
    schedule.run_pending()
    time.sleep(60)
