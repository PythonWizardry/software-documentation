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
