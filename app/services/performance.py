import redis
import json
from datetime import datetime
from app.repos.performance_repo import PerformanceRepo
from app.models.models import IndexPerformanceResponse
import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

class PerformanceError(Exception):
    pass

def validate_date(date_str: str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise PerformanceError(f"Invalid date format: {date_str}. Use YYYY-MM-DD.")

def get_index_performance(start_date: str, end_date: str):
    # -------------------------------
    # Validate dates
    # -------------------------------
    start_dt = validate_date(start_date)
    end_dt = validate_date(end_date)
    if start_dt > end_dt:
        raise PerformanceError("Start date must be earlier than end date.")

    # -------------------------------
    # Check Redis cache
    # -------------------------------
    key = f"index_performance:{start_date}:{end_date}"
    cached = r.get(key)
    if cached:
        data = json.loads(cached)
        return [IndexPerformanceResponse(**row) for row in data]

    # -------------------------------
    # Fetch from DB
    # -------------------------------
    df = PerformanceRepo.fetch_index_performance(start_date, end_date)

    if df.empty:
        return []

    result = [IndexPerformanceResponse(**row) for row in df.to_dict(orient="records")]

    # -------------------------------
    # Cache in Redis
    # -------------------------------
    r.setex(key, 3600, json.dumps([row.dict() for row in result]))

    return result
