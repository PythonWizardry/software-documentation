import json
from typing import Any, Dict, List, Optional

from src.strategy.output_strategy import OutputStrategy


class RedisStrategy(OutputStrategy):
    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        password: Optional[str],
        key_prefix: str,
        storage_type: str,
        ttl: Optional[int],
    ) -> None:
        self._key_prefix = key_prefix
        self._storage_type = storage_type
        self._ttl = ttl
        self._count = 0
        self._client = None

        try:
            import redis

            self._client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=True,
                socket_connect_timeout=5,
            )
            self._client.ping()
        except Exception:
            self._client = None

    def _make_key(self, record_id: Any) -> str:
        return f"{self._key_prefix}:{record_id}"

    def _get_record_id(self, record: Dict[str, Any]) -> str:
        for field in ("unique_key", "id", ":id:", "objectid"):
            if field in record:
                return str(record[field])
        return str(self._count)

    def write(self, record: Dict[str, Any]) -> None:
        self._count += 1
        if not self._client:
            return

        if self._storage_type == "hash":
            record_id = self._get_record_id(record)
            key = self._make_key(record_id)
            self._client.hset(key, mapping={k: str(v) for k, v in record.items()})
            if self._ttl:
                self._client.expire(key, self._ttl)
        elif self._storage_type == "stream":
            key = f"{self._key_prefix}:stream"
            self._client.xadd(key, {k: str(v) for k, v in record.items()}, maxlen=10000)
        else:
            key = f"{self._key_prefix}:list"
            self._client.rpush(key, json.dumps(record, ensure_ascii=False))
            if self._ttl:
                self._client.expire(key, self._ttl)

    def write_batch(self, records: List[Dict[str, Any]]) -> None:
        if not self._client:
            print("[Redis] Not connected. No records were written.")
            return
        for record in records:
            self.write(record)
        print(f"[Redis] Wrote {len(records)} records using '{self._storage_type}' storage.")

    def close(self) -> None:
        if self._client:
            self._client.close()
            print(f"[Redis] Connection closed. Total written: {self._count}.")
