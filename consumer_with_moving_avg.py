from kafka import KafkaConsumer
import json
from collections import deque
from datetime import datetime, timedelta

# Kafka configuration
KAFKA_TOPIC = "crypto_prices"
KAFKA_BROKER = "localhost:9092"

# Sliding window setup
window_size = 5  # Calculate 5-minute moving average
price_window = deque(maxlen=window_size)

# Initialize Kafka consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

print("Starting consumer with moving average calculation...")

# Function to calculate moving average
def calculate_moving_average(prices):
    return sum(prices) / len(prices) if prices else None

# Consume messages and calculate moving averages
try:
    for message in consumer:
        price_data = message.value
        price = price_data["price"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Add price to the sliding window
        price_window.append(price)

        # Calculate the moving average
        moving_avg = calculate_moving_average(price_window)

        print(f"Received: {price_data}")
        print(f"[{timestamp}] Moving Average (last {window_size} prices): {moving_avg:.2f}")
except KeyboardInterrupt:
    print("\nConsumer stopped.")
finally:
    consumer.close()
