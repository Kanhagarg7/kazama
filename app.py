import os
import redis
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

raw_uri = os.getenv("REDIS_URI")
password = os.getenv("REDIS_PASSWORD")

if not raw_uri or not password:
    raise ValueError("REDIS_URI or REDIS_PASSWORD not set in environment.")

# Build proper redis:// URI
redis_url = f"redis://:{password}@{raw_uri}"

# Connect and test
r = redis.from_url(redis_url)
r.set("time", "11 May 2025 04:41 PM")
print("Time set in Redis.")
