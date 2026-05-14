import json
from typing import Any, Dict, List

from src.strategy.output_strategy import OutputStrategy


class ConsoleStrategy(OutputStrategy):
    def __init__(self, pretty: bool = True) -> None:
        self._pretty = pretty
        self._count = 0

    def write(self, record: Dict[str, Any]) -> None:
        self._count += 1
        indent = 2 if self._pretty else None
        print(f"[#{self._count}] {json.dumps(record, ensure_ascii=False, indent=indent)}")

    def write_batch(self, records: List[Dict[str, Any]]) -> None:
        for record in records:
            self.write(record)

    def close(self) -> None:
        print(f"[Console] Printed {self._count} records")
