import os
import requests
from dotenv import load_dotenv

load_dotenv("key.env")

key = str(os.getenv('MBTA_API_KEY'))

print("\n Key: " + key + "\n")

url = "https://api-v3.mbta.com/vehicles"

params = { }

headers = {
    "x-api-header":key
}

response = requests.get(url, params=params, headers=headers)

print(response.status_code)
print(response.json())
