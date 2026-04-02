import argparse
import csv
import os
import random
from datetime import date, timedelta


class CSVGenerator:
    def __init__(self, filepath: str = "data/app_store_data.csv", rows: int = 1000) -> None:
        self.filepath = filepath
        self.rows = max(rows, 1000)

    def _random_date(self, start_year: int = 2024, end_year: int = 2026) -> date:
        start = date(start_year, 1, 1)
        end = date(end_year, 12, 31)
        delta_days = (end - start).days
        return start + timedelta(days=random.randint(0, delta_days))

    def _build_row(self, idx: int) -> dict:
        app_type = random.choice(["free_application", "paid_application"])
        has_review = random.choice([True, False])
        has_transaction = app_type == "paid_application" and random.choice([True, False])

        contains_ads = app_type == "free_application" and random.choice([True, False])
        price = round(random.uniform(0.99, 29.99), 2) if app_type == "paid_application" else ""

        release_date = self._random_date()
        review_date = self._random_date()
        transaction_date = self._random_date()

        developer_num = random.randint(1, 160)
        customer_num = random.randint(1, 600)
        app_num = random.randint(1, 350)

        return {
            "developer_username": f"dev_{developer_num}",
            "developer_email": f"dev_{developer_num}@example.com",
            "developer_name": f"Studio {developer_num}",
            "developer_website": f"https://studio-{developer_num}.dev",
            "customer_username": f"customer_{customer_num}",
            "customer_email": f"customer_{customer_num}@mail.com",
            "customer_payment_method": random.choice(["Card", "PayPal", "ApplePay", "GooglePay"]),
            "application_title": f"App {app_num}",
            "application_version": f"{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
            "application_type": app_type,
            "free_contains_ads": str(contains_ads),
            "paid_price": price,
            "release_version_tag": f"v{random.randint(1, 6)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
            "release_notes": f"Release notes batch {idx}",
            "release_date": release_date.isoformat(),
            "downloaded": str(random.choice([True, False])),
            "has_review": str(has_review),
            "review_rating": random.randint(1, 5) if has_review else "",
            "review_comment": f"Review text {idx}" if has_review else "",
            "review_date": review_date.isoformat() if has_review else "",
            "has_transaction": str(has_transaction),
            "transaction_id": f"TXN-{idx:05d}" if has_transaction else "",
            "transaction_amount": price if has_transaction else "",
            "transaction_date": transaction_date.isoformat() if has_transaction else "",
        }

    def generate_csv(self) -> str:
        directory = os.path.dirname(self.filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)

        fieldnames = [
            "developer_username",
            "developer_email",
            "developer_name",
            "developer_website",
            "customer_username",
            "customer_email",
            "customer_payment_method",
            "application_title",
            "application_version",
            "application_type",
            "free_contains_ads",
            "paid_price",
            "release_version_tag",
            "release_notes",
            "release_date",
            "downloaded",
            "has_review",
            "review_rating",
            "review_comment",
            "review_date",
            "has_transaction",
            "transaction_id",
            "transaction_amount",
            "transaction_date",
        ]

        with open(self.filepath, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for idx in range(1, self.rows + 1):
                writer.writerow(self._build_row(idx))

        return self.filepath


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate app-store CSV data (min 1000 rows).")
    parser.add_argument("--rows", type=int, default=1000, help="Number of rows to generate (minimum 1000).")
    parser.add_argument("--out", default="data/app_store_data.csv", help="Output CSV file path.")
    args = parser.parse_args()

    generator = CSVGenerator(filepath=args.out, rows=args.rows)
    output_path = generator.generate_csv()
    print(f"Generated {generator.rows} rows into {output_path}")


if __name__ == "__main__":
    main()
