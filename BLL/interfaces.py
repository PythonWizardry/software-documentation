from abc import ABC, abstractmethod

class IGooglePlayService(ABC):

    @abstractmethod
    def create_tables(self):
        pass

    @abstractmethod
    def paste_data(self):
        pass

    @abstractmethod
    def run_import(self):
        pass