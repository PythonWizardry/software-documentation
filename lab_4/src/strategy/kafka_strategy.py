import json
from typing import Any, Dict, List

from src.strategy.output_strategy import OutputStrategy


class KafkaStrategy(OutputStrategy):
    def __init__(self, bootstrap_servers: str, topic: str, client_id: str) -> None:
        self._topic = topic
        self._count = 0
        self._producer = None

        try:
            from kafka import KafkaProducer

            self._producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                client_id=client_id,
                value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode("utf-8"),
                retries=3,
                acks="all",
            )
        except Exception:
            self._producer = None

    def write(self, record: Dict[str, Any]) -> None:
        self._count += 1
        if not self._producer:
            return
        self._producer.send(self._topic, value=record)

    def write_batch(self, records: List[Dict[str, Any]]) -> None:
        if not self._producer:
            print("[Kafka] Not connected. No records were sent.")
            return
        for record in records:
            self.write(record)
        self._producer.flush()
        print(f"[Kafka] Sent {len(records)} records to topic '{self._topic}'.")

    def close(self) -> None:
        if self._producer:
            self._producer.flush()
            self._producer.close()
            print(f"[Kafka] Connection closed. Total sent: {self._count}.")
