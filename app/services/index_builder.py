from datetime import datetime
from typing import List, Tuple
from app.repos.index_repo import IndexRepository
from app.models.models import BuildIndexRequest, BuildIndexResponse

class IndexBuildError(Exception):
    pass

def build_index_service(request: BuildIndexRequest) -> BuildIndexResponse:
    start_date = request.start_date
    end_date = request.end_date

    # -------------------------------
    # Validate date format and range
    # -------------------------------
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise IndexBuildError("Date format incorrect. Use YYYY-MM-DD.")

    if start_dt >= end_dt:
        raise IndexBuildError("Start date must be earlier than end date.")

    if (end_dt - start_dt).days > 40:
        raise IndexBuildError("Date range cannot exceed 40 days.")

    # -------------------------------
    # Fetch stock prices
    # -------------------------------
    df = IndexRepository.fetch_stock_prices(start_date, end_date)
    if df.empty:
        raise IndexBuildError("No stock price data found for the given date range.")

    # -------------------------------
    # Build index
    # -------------------------------
    compositions: List[Tuple[str, int, float]] = []
    perf_rows: List[Tuple[str, float, float, float]] = []

    base_level = 100.0
    prev_index = base_level
    prev_prices = {}

    for date, group in df.groupby("date"):
        top100 = group.head(100).copy()
        top100["weight"] = 1.0 / 100

        for _, row in top100.iterrows():
            compositions.append((date, row["stock_id"], row["weight"]))

        daily_return = 0
        for _, row in top100.iterrows():
            sid = row["stock_id"]
            price = row["close_price"]
            if sid in prev_prices:
                daily_return += row["weight"] * ((price / prev_prices[sid]) - 1)
            prev_prices[sid] = price

        index_level = prev_index * (1 + daily_return)
        cum_return = (index_level / base_level) - 1

        perf_rows.append((date, index_level, daily_return, cum_return))
        prev_index = index_level

    # -------------------------------
    # Save to DB
    # -------------------------------
    IndexRepository.save_compositions(compositions)
    IndexRepository.save_performance(perf_rows)
    IndexRepository.invalidate_cache()

    return BuildIndexResponse(message="Index built", days=len(perf_rows))
