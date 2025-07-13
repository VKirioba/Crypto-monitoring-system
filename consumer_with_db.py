from kafka import KafkaConsumer
import json
from collections import defaultdict, deque
from datetime import datetime
import psycopg2

# Kafka configuration
KAFKA_TOPIC = "crypto_prices"
KAFKA_BROKER = "localhost:9092"

# TimescaleDB connection configuration
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"

# Connect to TimescaleDB
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

# Ensure the crypto_prices table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS crypto_prices (
    time TIMESTAMPTZ NOT NULL,
    currency TEXT NOT NULL,
    price DOUBLE PRECISION,
    moving_avg DOUBLE PRECISION,
    PRIMARY KEY (time, currency)
);
""")
conn.commit()

# Initialize Kafka consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

print("Starting Kafka consumer...")

# Sliding window setup for moving averages
window_size = 5  # Number of prices to calculate the moving average
price_windows = defaultdict(lambda: deque(maxlen=window_size))  # One sliding window per currency

# Save data to TimescaleDB
def save_to_db(timestamp, currency, price, moving_avg):
    cursor.execute("""
    INSERT INTO crypto_prices (time, currency, price, moving_avg)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (time, currency) DO NOTHING;
    """, (timestamp, currency, price, moving_avg))
    conn.commit()

# Function to calculate moving average
def calculate_moving_average(prices):
    return sum(prices) / len(prices) if prices else None

# Consume messages from Kafka
try:
    for message in consumer:
        price_data = message.value
        timestamp = datetime.now()  # Use the current timestamp
        currency = price_data.get("currency", "BTC")  # Default to BTC
        price = price_data.get("price", 0.0)

        # Update the sliding window for the currency
        price_windows[currency].append(price)

        # Calculate the moving average
        moving_avg = calculate_moving_average(price_windows[currency])

        print(f"Received data: {price_data}")
        print(f"Calculated moving average for {currency}: {moving_avg}")

        # Save the price and moving average to the database
        save_to_db(timestamp, currency, price, moving_avg)
        print(f"Saved to database: {currency} - Price: {price}, Moving Average: {moving_avg}")

except KeyboardInterrupt:
    print("\nStopping consumer...")
finally:
    consumer.close()
    cursor.close()
    conn.close()
