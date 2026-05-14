# Lab 4 - Strategy Pattern

Goal: read data from the assigned dataset and output it using a Strategy pattern.
Output target must be switchable via config only (no code changes).

## Features
- Dataset reader is separated from output logic.
- Strategy-based outputs: console, Kafka, Redis.
- Configurable via YAML.
- Optional docker-compose for Kafka/Redis.

## Quick start
1) Create and activate a virtual env
2) Install dependencies:
   pip install -r requirements.txt
3) Run:
   python -m src.main

## Configuration
Edit config/config.yaml:
- output.strategy: console | kafka | redis (firebase can be added later)
- dataset.url: Socrata API endpoint
- dataset.local_path: local CSV cache path

## Docker (optional)
To start Kafka and Redis for testing:
  docker-compose up -d

Then set output.strategy in config.yaml to kafka or redis.

## Verification checklist
Console mode:
- Set output.strategy: console
- Run: python -m src.main
- Expect JSON records printed to terminal

Redis mode:
- Set output.strategy: redis
- Run: python -m src.main
- Check Redis list length and sample values:
   docker exec -it lab_4-redis-1 redis-cli
   LLEN nypd_shootings:list
   LRANGE nypd_shootings:list 0 2

Kafka mode:
- Set output.strategy: kafka
- Run: python -m src.main
- Consume a few messages from the topic:
   docker exec -it lab_4-kafka-1 kafka-console-consumer --bootstrap-server localhost:9092 --topic nypd_shootings --from-beginning --max-messages 3

## Firebase (future)
Add a new strategy class (firebase_strategy.py) and update strategy_factory.py.
No changes are needed in reader or main.
