from typing import Any, Dict

from src.strategy.console_strategy import ConsoleStrategy
from src.strategy.kafka_strategy import KafkaStrategy
from src.strategy.redis_strategy import RedisStrategy
from src.strategy.output_strategy import OutputStrategy


def create_strategy(config: Dict[str, Any]) -> OutputStrategy:
    name = config.get("output", {}).get("strategy", "console").lower()

    if name == "console":
        return ConsoleStrategy(pretty=True)

    if name == "kafka":
        kafka_cfg = config.get("kafka", {})
        return KafkaStrategy(
            bootstrap_servers=kafka_cfg.get("bootstrap_servers", "localhost:9092"),
            topic=kafka_cfg.get("topic", "nypd_shootings"),
            client_id=kafka_cfg.get("client_id", "lab4_producer"),
        )

    if name == "redis":
        redis_cfg = config.get("redis", {})
        return RedisStrategy(
            host=redis_cfg.get("host", "localhost"),
            port=redis_cfg.get("port", 6379),
            db=redis_cfg.get("db", 0),
            password=redis_cfg.get("password"),
            key_prefix=redis_cfg.get("key_prefix", "nypd_shootings"),
            storage_type=redis_cfg.get("storage_type", "list"),
            ttl=redis_cfg.get("ttl"),
        )

    raise ValueError(f"Unknown strategy: {name}")
