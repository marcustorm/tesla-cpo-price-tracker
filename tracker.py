import requests
import json
import time
from datetime import datetime, timezone

# Tesla API URL
TESLA_API_URL = "https://www.tesla.com/inventory/api/v1/inventory-results"

# Query parameters
payload = {
    "query": {
        "model": "m3",
        "condition": "used",
        "options": {
            "TRIM": ["MRRWD", "LRRWD", "LRAWD"],  # All Model 3 trims
        },
        "arrangeby": "Price",
        "order": "asc",
        "market": "CH",  # Switzerland
        "language": "de",
        "super_region": "europe",
        "lng": 8.5417,  # Zurich coordinates
        "lat": 47.3769,
        "zip": "8001",
        "range": 0
    },
    "offset": 0,
    "count": 50,  # Fetch 50 results per request
    "outsideOffset": 0,
    "outsideSearch": False
}

# Headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

# Retry mechanism in case of failure
MAX_RETRIES = 5
for attempt in range(MAX_RETRIES):
    try:
        response = requests.get(TESLA_API_URL, headers=headers, params={"query": json.dumps(payload)}, timeout=10)
        response.raise_for_status()  # Raises an error if request fails
        data = response.json()

        # Save data with UTC timestamp
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        filename = f"data/{date_str}.json"
        with open(filename, "w") as file:
            json.dump(data, file, indent=2)

        print(f"✅ Data saved successfully: {filename}")
        break  # Exit loop on success

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Attempt {attempt + 1} failed: {e}")
        time.sleep(5)  # Wait before retrying

