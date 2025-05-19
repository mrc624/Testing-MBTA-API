import os
from dotenv import load_dotenv

load_dotenv("key.env")

key = str(os.getenv('MBTA_API_KEY'))

print("\n Key: " + key + "\n")