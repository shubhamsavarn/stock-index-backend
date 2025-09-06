import redis
import os
import time

# -------------------------------
# Environment-aware configuration
# -------------------------------
# Default host is 'localhost' (for local dev),
# inside Docker use 'redis' (set via REDIS_HOST env)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# -------------------------------
# Redis connection with retry
# -------------------------------
MAX_RETRIES = 5
RETRY_DELAY = 2  # seconds

for attempt in range(1, MAX_RETRIES + 1):
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        r.ping()  # Test connection
        print(f"[Redis] Connected to {REDIS_HOST}:{REDIS_PORT}")
        break
    except redis.ConnectionError as e:
        print(f"[Redis] Attempt {attempt}/{MAX_RETRIES} failed: {e}")
        time.sleep(RETRY_DELAY)
else:
    raise Exception(f"Cannot connect to Redis at {REDIS_HOST}:{REDIS_PORT} after {MAX_RETRIES} attempts")
