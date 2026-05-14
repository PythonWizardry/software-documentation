import csv
import json
import os
import urllib.parse
import urllib.request
from typing import Any, Dict, List


class DatasetReader:
    def __init__(self, api_url: str, local_path: str, limit: int = 200) -> None:
        self._api_url = api_url
        self._local_path = local_path
        self._limit = limit

    def fetch_and_save(self) -> str:
        os.makedirs(os.path.dirname(self._local_path) or ".", exist_ok=True)

        params = urllib.parse.urlencode({"$limit": self._limit, "$order": ":id"})
        url = f"{self._api_url}?{params}"

        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "lab4-strategy/1.0",
            },
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read().decode("utf-8")
            records: List[Dict[str, Any]] = json.loads(raw)

        if not records:
            raise ValueError("Dataset is empty")

        fieldnames = list(records[0].keys())
        with open(self._local_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(records)

        return self._local_path

    def read(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self._local_path):
            self.fetch_and_save()

        records: List[Dict[str, Any]] = []
        with open(self._local_path, "r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                clean_row = {k: v for k, v in row.items() if v != ""}
                records.append(clean_row)

        return records
