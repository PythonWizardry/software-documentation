from abc import ABC, abstractmethod

class ICSVReader(ABC):
    @abstractmethod
    def read_from_csv(self):
        pass

class IDBRepository(ABC):
    @abstractmethod
    def paste_all_data(self, rows):
        pass

    @abstractmethod
    def list_applications(self):
        pass

    @abstractmethod
    def get_application(self, app_id: int):
        pass

    @abstractmethod
    def create_application(self, payload: dict):
        pass

    @abstractmethod
    def update_application(self, app_id: int, payload: dict):
        pass

    @abstractmethod
    def delete_application(self, app_id: int):
        pass

class IDBModels(ABC):
    @abstractmethod
    def create_tables(self):
        pass