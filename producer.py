from kafka import KafkaProducer
import requests
import json
import time

# Coinbase API endpoint
COINBASE_URL_TEMPLATE = "https://api.coinbase.com/v2/prices/{currency}-USD/spot"

# Cryptocurrencies to fetch
CRYPTOCURRENCIES = ["BTC", "ETH", "LTC"]  # Add more if needed

# Kafka configuration
KAFKA_TOPIC = "crypto_prices"
KAFKA_BROKER = "localhost:9092"

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize messages to JSON
)

# Function to fetch cryptocurrency price
def fetch_crypto_price(currency):
    try:
        url = COINBASE_URL_TEMPLATE.format(currency=currency)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            price = float(data["data"]["amount"])
            return {"currency": currency, "price": price}
        else:
            print(f"Failed to fetch {currency} data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching {currency} price: {e}")
        return None

# Continuously fetch data and publish to Kafka
try:
    print("Starting producer...")
    while True:
        for currency in CRYPTOCURRENCIES:
            price_data = fetch_crypto_price(currency)
            if price_data:
                producer.send(KAFKA_TOPIC, value=price_data)
                print(f"Published to Kafka: {price_data}")
        time.sleep(5)  # Fetch data every 5 seconds
except KeyboardInterrupt:
    print("\nStopping producer...")
finally:
    producer.close()
