from .interfaces import IGooglePlayService
from DAL.interfaces import ICSVReader, IDBModels, IDBRepository


class GooglePlayService(IGooglePlayService):
    def __init__(self, csv_reader: ICSVReader, db_models: IDBModels, db_repository: IDBRepository):
        self.csv_reader = csv_reader
        self.db_models = db_models
        self.db_repository = db_repository

    def create_tables(self):
        self.db_models.create_tables()

    def paste_data(self):
        rows = self.csv_reader.read_from_csv()
        self.db_repository.paste_all_data(rows)

    def run_import(self):
        self.create_tables()
        self.paste_data()

    def list_applications(self):
        return self.db_repository.list_applications()

    def get_application(self, app_id: int):
        return self.db_repository.get_application(app_id)

    def create_application(self, payload: dict):
        app_type = payload.get("application_type")
        if app_type not in {"free_application", "paid_application"}:
            raise ValueError("Invalid application_type. Use free_application or paid_application.")

        title = (payload.get("title") or "").strip()
        version = (payload.get("version") or "").strip()
        if not title or not version:
            raise ValueError("Title and version are required.")

        email = (payload.get("developer_email") or "").strip()
        username = (payload.get("developer_username") or "").strip()
        developer_name = (payload.get("developer_name") or "").strip()
        if not email or not username or not developer_name:
            raise ValueError("Developer username, email and name are required.")

        normalized_payload = {
            "application_type": app_type,
            "title": title,
            "version": version,
            "developer_username": username,
            "developer_email": email,
            "developer_name": developer_name,
            "developer_website": (payload.get("developer_website") or "").strip() or None,
            "contains_ads": bool(payload.get("contains_ads", False)),
            "price": float(payload.get("price", 0) or 0),
        }

        if app_type == "paid_application" and normalized_payload["price"] <= 0:
            raise ValueError("Paid application price must be greater than 0.")

        return self.db_repository.create_application(normalized_payload)

    def update_application(self, app_id: int, payload: dict):
        app = self.db_repository.get_application(app_id)
        if app is None:
            return None

        app_type = payload.get("application_type")
        if app_type not in {"free_application", "paid_application"}:
            raise ValueError("Invalid application_type. Use free_application or paid_application.")

        title = (payload.get("title") or "").strip()
        version = (payload.get("version") or "").strip()
        if not title or not version:
            raise ValueError("Title and version are required.")

        normalized_payload = {
            "title": title,
            "version": version,
            "application_type": app_type,
            "contains_ads": bool(payload.get("contains_ads", False)),
            "price": float(payload.get("price", 0) or 0),
        }

        if app_type == "paid_application" and normalized_payload["price"] <= 0:
            raise ValueError("Paid application price must be greater than 0.")

        return self.db_repository.update_application(app_id, normalized_payload)

    def delete_application(self, app_id: int):
        return self.db_repository.delete_application(app_id)
