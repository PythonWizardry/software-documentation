from pathlib import Path

from fastapi import FastAPI, HTTPException, Query

from BLL.service import GooglePlayService
from DAL import engine, session
from DAL.csv_reader import CSVReader
from DAL.db_models import Base, DBModels
from DAL.db_repository import DBRepository
from generator.csv_generator import CSVGenerator


app = FastAPI(
    title="Google Play Import API",
    description="Lab 2 API for CSV generation and import into SQLite.",
    version="1.0.0",
)


def build_service(csv_path: str, delimiter: str = ",") -> GooglePlayService:
    csv_reader = CSVReader(csv_path, delimiter=delimiter)
    db_models = DBModels(engine)
    db_repository = DBRepository(session)
    return GooglePlayService(csv_reader, db_models, db_repository)


@app.post("/clear-data")
def clear_data() -> dict:
    try:
        session.rollback()
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Clear data failed: {exc}") from exc

    return {"message": "All database data cleared successfully."}


@app.post("/generate-csv")
def generate_csv(
    rows: int = Query(1000, ge=1, description="Requested row count. Minimum output is 1000."),
    csv_path: str = Query("data/app_store_data.csv", description="Output CSV path."),
    delimiter: str = Query(",", min_length=1, max_length=2, description="CSV delimiter. Use \\t for tab."),
) -> dict:
    try:
        output = CSVGenerator(filepath=csv_path, rows=rows, delimiter=delimiter).generate_csv()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "message": "CSV generated successfully.",
        "requested_rows": rows,
        "generated_rows": max(rows, 1000),
        "delimiter": delimiter,
        "csv_path": output,
    }


@app.post("/import-data")
def import_data(
    csv_path: str = Query("data/app_store_data.csv", description="CSV path to import."),
    delimiter: str = Query(",", min_length=1, max_length=2, description="CSV delimiter used in file. Use \\t for tab."),
    generate_if_missing: bool = Query(
        False,
        description="Generate the CSV file first when it is missing.",
    ),
    rows_if_generated: int = Query(
        1000,
        ge=1,
        description="Requested row count when generate_if_missing=true.",
    ),
) -> dict:
    csv_file = Path(csv_path)

    if not csv_file.exists() and generate_if_missing:
        try:
            CSVGenerator(filepath=csv_path, rows=rows_if_generated, delimiter=delimiter).generate_csv()
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    if not csv_file.exists():
        raise HTTPException(status_code=404, detail=f"CSV file not found: {csv_path}")

    try:
        service = build_service(str(csv_file), delimiter=delimiter)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        service.run_import()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Import failed: {exc}") from exc

    return {
        "message": "Import completed successfully.",
        "csv_path": str(csv_file),
        "delimiter": delimiter,
    }
