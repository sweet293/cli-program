import json
import os
import hashlib
from datetime import datetime, timedelta
from searchreq import search_request

CACHE_DIR = 'cache'
CACHE_EXPIRY = timedelta(hours = 2)

def get_cache_file_path(query):
    os.makedirs(CACHE_DIR, exist_ok=True)
    query_hash = hashlib.md5(query.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{query_hash}.json")

def is_cache_valid(timestamp_str):
    cache_time = datetime.fromisoformat(timestamp_str)
    return datetime.now() - cache_time < CACHE_EXPIRY

def get_search_results(query):
    cache_file = get_cache_file_path(query)

    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
            if is_cache_valid(cache_data.get("timestamp", "")):
                print("Loading from cache...")
                return cache_data["results"]

    print("Scraping new results...")
    results = search_request(query)  # <-- your scraping function

    cache_data = {
        "timestamp": datetime.now().isoformat(),
        "results": results
    }

    with open(cache_file, 'w') as f:
        json.dump(cache_data, f, indent=2)
        print("Saved to cache")

    return results