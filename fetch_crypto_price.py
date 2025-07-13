import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API credentials
API_KEY = os.getenv("COINBASE_API_KEY")
API_SECRET = os.getenv("COINBASE_API_SECRET")

# Fetch Bitcoin price using Coinbase API
def fetch_crypto_price():
    url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
    headers = {
        "CB-ACCESS-KEY": API_KEY,
        "CB-ACCESS-SIGN": API_SECRET,  # Not always required for public price endpoints
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"Bitcoin Price: {data['data']['amount']} USD")
    else:
        print(f"Failed to fetch price data. Status Code: {response.status_code}")

fetch_crypto_price()
