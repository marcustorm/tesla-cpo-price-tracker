import requests
import json
from datetime import datetime

# Define the API endpoint
url = "https://www.tesla.com/inventory/api/v1/inventory-results"

# Define the request payload
payload = {
    "query": {
        "model": "m3",
        "condition": "used",
        "options": {},
        "arrangeby": "Price",
        "order": "asc",
        "market": "CH",
        "language": "de",
        "super_region": "europe",
        "lng": 8.5417,  # Longitude for Zurich
        "lat": 47.3769,  # Latitude for Zurich
        "zip": "8000",  # Postal code for Zurich
        "range": 0
    },
    "offset": 0,
    "count": 50,
    "outsideOffset": 0,
    "outsideSearch": False
}

# Set headers
headers = {
    "Content-Type": "application/json"
}

# Send the POST request
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    # Extract vehicle results
    vehicles = data.get('results', [])
    if vehicles:
        # Create a filename with the current date
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        filename = f"tesla_used_inventory_{date_str}.json"
        # Save the data to a JSON file
        with open(filename, 'w') as f:
            json.dump(vehicles, f, indent=4)
        print(f"Data saved to {filename}")
    else:
        print("No vehicles found.")
else:
    print(f"Failed to retrieve data: {response.status_code}")
