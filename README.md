<<<<<<< HEAD
 Cryptocurrency Monitoring System

 Overview
This project tracks real-time cryptocurrency prices (BTC, ETH, LTC) and provides actionable insights using moving averages. The data is visualized in Grafana dashboards.

Setup
	1. Install Docker and ensure it's running.
	2. Clone this repository:
   		bash
   		git clone <repository-url>
  		cd crypto-monitoring-project


Start the services:
	docker-compose up -d

Run the Python scripts:
	python producer.py
	python consumer_with_db.py
Access
    Grafana: http://localhost:3000 (username: admin, password: admin).

=======
# Crypto-monitoring-system
This project is a real-time cryptocurrency monitoring system tracking Bitcoin (BTC), Ethereum (ETH), and Litecoin (LTC) via the Coinbase API. It streams data through Kafka, stores it in TimescaleDB for analysis, and visualizes trends in Grafana, providing actionable insights into cryptocurrency markets.
>>>>>>> 6529e4443010af0fd16732f8eede1ecc1f72a209
