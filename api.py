from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Query, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

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
templates = Jinja2Templates(directory="templates")


def build_service(csv_path: str, delimiter: str = ",") -> GooglePlayService:
    csv_reader = CSVReader(csv_path, delimiter=delimiter)
    db_models = DBModels(engine)
    db_repository = DBRepository(session)
    return GooglePlayService(csv_reader, db_models, db_repository)


def build_mvc_service() -> GooglePlayService:
    db_models = DBModels(engine)
    db_repository = DBRepository(session)
    # csv_reader is not used for MVC flows, so a placeholder path is sufficient.
    return GooglePlayService(CSVReader("data/app_store_data.csv"), db_models, db_repository)


def _bool_from_form(value: str | None) -> bool:
    return value in {"1", "true", "on", "yes"}


@app.on_event("startup")
def startup_event() -> None:
    DBModels(engine).create_tables()


@app.get("/")
def root_redirect() -> RedirectResponse:
    return RedirectResponse(url="/applications", status_code=303)


@app.get("/applications")
def list_applications(request: Request):
    service = build_mvc_service()
    applications = service.list_applications()
    return templates.TemplateResponse(
        request,
        "applications_list.html",
        {"applications": applications},
    )


@app.get("/applications/create")
def create_application_form(request: Request):
    return templates.TemplateResponse(
        request,
        "application_form.html",
        {
            "form_mode": "create",
            "action_url": "/applications/create",
            "application": None,
            "error": None,
        },
    )


@app.post("/applications/create")
def create_application(
    request: Request,
    title: str = Form(...),
    version: str = Form(...),
    application_type: str = Form(...),
    price: float = Form(0),
    contains_ads: str | None = Form(None),
    developer_username: str = Form(...),
    developer_email: str = Form(...),
    developer_name: str = Form(...),
    developer_website: str = Form(""),
):
    service = build_mvc_service()
    payload = {
        "title": title,
        "version": version,
        "application_type": application_type,
        "price": price,
        "contains_ads": _bool_from_form(contains_ads),
        "developer_username": developer_username,
        "developer_email": developer_email,
        "developer_name": developer_name,
        "developer_website": developer_website,
    }
    try:
        service.create_application(payload)
    except ValueError as exc:
        return templates.TemplateResponse(
            request,
            "application_form.html",
            {
                "form_mode": "create",
                "action_url": "/applications/create",
                "application": payload,
                "error": str(exc),
            },
            status_code=400,
        )

    return RedirectResponse(url="/applications", status_code=303)


@app.get("/applications/{app_id}")
def application_details(request: Request, app_id: int):
    service = build_mvc_service()
    application = service.get_application(app_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return templates.TemplateResponse(
        request,
        "application_details.html",
        {"application": application},
    )


@app.get("/applications/{app_id}/edit")
def edit_application_form(request: Request, app_id: int):
    service = build_mvc_service()
    application = service.get_application(app_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return templates.TemplateResponse(
        request,
        "application_form.html",
        {
            "form_mode": "edit",
            "action_url": f"/applications/{app_id}/edit",
            "application": application,
            "error": None,
        },
    )


@app.post("/applications/{app_id}/edit")
def edit_application(
    request: Request,
    app_id: int,
    title: str = Form(...),
    version: str = Form(...),
    application_type: str = Form(...),
    price: float = Form(0),
    contains_ads: str | None = Form(None),
):
    service = build_mvc_service()
    current_application = service.get_application(app_id)
    if current_application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    payload = {
        "title": title,
        "version": version,
        "application_type": application_type,
        "price": price,
        "contains_ads": _bool_from_form(contains_ads),
    }

    try:
        service.update_application(app_id, payload)
    except ValueError as exc:
        return templates.TemplateResponse(
            request,
            "application_form.html",
            {
                "form_mode": "edit",
                "action_url": f"/applications/{app_id}/edit",
                "application": payload,
                "error": str(exc),
            },
            status_code=400,
        )

    return RedirectResponse(url=f"/applications/{app_id}", status_code=303)


@app.post("/applications/{app_id}/delete")
def delete_application(app_id: int):
    service = build_mvc_service()
    deleted = service.delete_application(app_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Application not found")
    return RedirectResponse(url="/applications", status_code=303)


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
