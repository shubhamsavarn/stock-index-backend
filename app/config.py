import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "stock_data.sqlite")
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
