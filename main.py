import argparse
import os

from BLL.service import GooglePlayService
from DAL import engine, session
from DAL.csv_reader import CSVReader
from DAL.db_models import DBModels
from DAL.db_repository import DBRepository
from generator.csv_generator import CSVGenerator


def build_service(csv_path: str) -> GooglePlayService:
    csv_reader = CSVReader(csv_path)
    db_models = DBModels(engine)
    db_repository = DBRepository(session)
    return GooglePlayService(csv_reader, db_models, db_repository)


def main() -> None:
    parser = argparse.ArgumentParser(description="Import app-store CSV data into SQLite using 3-layer architecture.")
    parser.add_argument("--csv", default="data/app_store_data.csv", help="CSV file path to import.")
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Generate CSV before importing (minimum 1000 rows).",
    )
    parser.add_argument("--rows", type=int, default=1000, help="Rows to generate when --generate is used.")
    args = parser.parse_args()

    if args.generate:
        print(f"Generating CSV with {args.rows} rows at {args.csv}...")
        output = CSVGenerator(filepath=args.csv, rows=args.rows).generate_csv()
        print(f"CSV generated: {output}")

    # if not os.path.exists(args.csv):
    #     raise FileNotFoundError(f"CSV file not found: {args.csv}")
    
    if not os.path.exists(args.csv):
        args.csv = "C:\\EVERYTHING\\CODE\\Documenting\\software-documentation\\data\\app_store_data.csv"
        if not os.path.exists(args.csv):
            raise FileNotFoundError(f"CSV file not found: {args.csv}")


    service = build_service(args.csv)
    print("Starting import process...")
    service.run_import()
    print("Import completed successfully.")


if __name__ == "__main__":
    main()
