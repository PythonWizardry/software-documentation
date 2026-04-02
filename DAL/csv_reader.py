import csv
from datetime import datetime

from .interfaces import ICSVReader


class CSVReader(ICSVReader):
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    @staticmethod
    def _to_bool(value: str):
        if value is None:
            return None
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes"}:
            return True
        if lowered in {"false", "0", "no"}:
            return False
        return None

    @staticmethod
    def _to_int(value: str):
        if value is None or value == "":
            return None
        return int(value)

    @staticmethod
    def _to_float(value: str):
        if value is None or value == "":
            return None
        return float(value)

    @staticmethod
    def _to_date(value: str):
        if value is None or value == "":
            return None
        return datetime.strptime(value, "%Y-%m-%d").date()

    def read_from_csv(self):
        data = []
        with open(self.filepath, mode="r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for raw in reader:
                row = {
                    "developer_username": raw["developer_username"],
                    "developer_email": raw["developer_email"],
                    "developer_name": raw["developer_name"],
                    "developer_website": raw["developer_website"],
                    "customer_username": raw["customer_username"],
                    "customer_email": raw["customer_email"],
                    "customer_payment_method": raw["customer_payment_method"],
                    "application_title": raw["application_title"],
                    "application_version": raw["application_version"],
                    "application_type": raw["application_type"],
                    "free_contains_ads": self._to_bool(raw["free_contains_ads"]),
                    "paid_price": self._to_float(raw["paid_price"]),
                    "release_version_tag": raw["release_version_tag"],
                    "release_notes": raw["release_notes"],
                    "release_date": self._to_date(raw["release_date"]),
                    "downloaded": self._to_bool(raw["downloaded"]),
                    "has_review": self._to_bool(raw["has_review"]),
                    "review_rating": self._to_int(raw["review_rating"]),
                    "review_comment": raw["review_comment"] or None,
                    "review_date": self._to_date(raw["review_date"]),
                    "has_transaction": self._to_bool(raw["has_transaction"]),
                    "transaction_id": raw["transaction_id"] or None,
                    "transaction_amount": self._to_float(raw["transaction_amount"]),
                    "transaction_date": self._to_date(raw["transaction_date"]),
                }
                data.append(row)
        return data
