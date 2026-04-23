# software-documentation
This repository contains my lab assignments for the course "Software Documentation and Design Patterns"

## Software Documentation - Lab 2

This project implements a 3-layer server-side architecture for importing app store data from CSV into a SQLite database using SQLAlchemy ORM.

## What Is Implemented

- Data Access Layer (DAL):
	- ORM models based on UML class diagram (inheritance + relationships)
	- CSV reader
	- Repository for saving parsed data into database
- Business Logic Layer (BLL):
	- Service that orchestrates table creation and data import
	- Depends on DAL interfaces (Dependency Injection)
- Presentation Layer (PL):
	- Interface-only layer (as required by assignment)
- CSV Generator:
	- Separate module/class runnable from command line
	- Generates one CSV file with minimum 1000 rows

## Project Structure

- [BLL](BLL)
- [DAL](DAL)
- [PL](PL)
- [generator](generator)
- [data](data)
- [main.py](main.py)

## How To Run

1. Create and activate virtual environment (optional but recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run full flow (generate CSV + import to DB):

```bash
python main.py --generate --rows 1000
```

Example with custom delimiter (`;`):

```bash
python main.py --generate --rows 1000 --delimiter ";" --csv data/app_store_data.csv
```

4. Import from existing CSV only:

```bash
python main.py --csv data/app_store_data.csv
```

If your CSV uses tab as delimiter:

```bash
python main.py --csv data/app_store_data.csv --delimiter "\t"
```

## FastAPI + Swagger

Run API server:

```bash
uvicorn api:app --reload
```

Open Swagger UI in browser:

- http://127.0.0.1:8000/docs

Main endpoints:

- GET `/health`
- POST `/generate-csv`
- POST `/import-data`

Delimiter examples in Swagger / query:

- Generate with semicolon: `/generate-csv?rows=1000&delimiter=;`
- Import semicolon CSV: `/import-data?csv_path=data/app_store_data.csv&delimiter=;`
- Use tab delimiter: pass `delimiter=\t`

## Software Documentation - Lab 3 (MVC Web App)

Main entity for MVC part: **Application** (Google Play Store domain).

Implemented according to assignment:

- MVC controllers (FastAPI routes) for Application entity
- Model and DB interaction through SQLAlchemy + repository
- Business logic layer is used by controllers for data read/write
- CRUD operations: create, read, update, delete
- HTML views rendered with Jinja2 templates

### MVC Routes

- GET `/` -> redirect to applications page
- GET `/applications` -> list applications (HTML)
- GET `/applications/create` -> create form (HTML)
- POST `/applications/create` -> create application
- GET `/applications/{app_id}` -> details page (HTML)
- GET `/applications/{app_id}/edit` -> edit form (HTML)
- POST `/applications/{app_id}/edit` -> update application
- POST `/applications/{app_id}/delete` -> delete application

### Run MVC App

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run server:

```bash
uvicorn api:app --reload
```

3. Open browser:

- MVC pages: http://127.0.0.1:8000/applications
- Swagger API: http://127.0.0.1:8000/docs

## Notes

- The generator enforces minimum 1000 rows.
- Database file is created locally as SQLite.


-Vety important note:
🧐🧐🧐You must use the same delimiter when generating csv and then when importing to DB
