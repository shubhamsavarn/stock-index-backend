import redis
import json

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Keys for different endpoints
keys = [
    "index_comp:2025-08-27",
    "comp_changes:2025-08-21:2025-09-04"
]


for key in keys:
    cached_data = r.get(key)
    if cached_data:
        print(f"\nCache for {key}:")
        try:
            data = json.loads(cached_data)
            print(json.dumps(data, indent=4))  # pretty-print JSON
        except json.JSONDecodeError:
            print(cached_data)
    else:
        print(f"\nNo cache found for {key}")
