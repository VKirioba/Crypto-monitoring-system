from kafka import KafkaConsumer
import json

# Kafka configuration
KAFKA_TOPIC = "crypto_prices"
KAFKA_BROKER = "localhost:9092"

# Initialize Kafka consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))  # Deserialize JSON messages
)

print("Starting consumer...")

# Consume messages from the Kafka topic
try:
    for message in consumer:
        price_data = message.value  # Access the deserialized message
        print(f"Received: {price_data}")
except KeyboardInterrupt:
    print("\nConsumer stopped.")
finally:
    consumer.close()
