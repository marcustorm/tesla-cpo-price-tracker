import requests
import json
import time
from datetime import datetime, timezone

url = "https://www.tesla.com/inventory/api/v1/inventory-results"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

payload = {
    "query": {},  # Modify based on Tesla's API
    "options": {},
}

# Retry mechanism
MAX_RETRIES = 5
for attempt in range(MAX_RETRIES):
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()  # Raises an error for HTTP 4xx/5xx
        data = response.json()
        
        # Save data with UTC timestamp
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        with open(f"data/{date_str}.json", "w") as file:
            json.dump(data, file, indent=2)
        
        print("✅ Data scraped successfully!")
        break  # Exit loop on success

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Attempt {attempt + 1} failed: {e}")
        time.sleep(5)  # Wait before retrying

