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
pip install -r requirements.txt.
```

3. Run full flow (generate CSV + import to DB):

```bash
python main.py --generate --rows 1000
```

4. Import from existing CSV only:

```bash
python main.py --csv data/app_store_data.csv
```

## Notes

- The generator enforces minimum 1000 rows.
- Database file is created locally as SQLite.
