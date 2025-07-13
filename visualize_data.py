import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

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

# Fetch data from TimescaleDB
query = """
SELECT time, currency, price
FROM crypto_prices
ORDER BY time ASC;
"""
df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Convert time to a datetime object
df['time'] = pd.to_datetime(df['time'])

# Plot the data
plt.figure(figsize=(12, 6))
for currency in df['currency'].unique():
    currency_data = df[df['currency'] == currency]
    plt.plot(currency_data['time'], currency_data['price'], label=currency)

plt.title('Cryptocurrency Prices Over Time')
plt.xlabel('Time')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Display the plot
plt.show()
