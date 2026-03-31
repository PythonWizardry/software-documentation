from abc import ABC, abstractmethod

class ICSVReader(ABC):
    @abstractmethod
    def read_from_csv(self):
        pass 

class IDBRepository(ABC):
    @abstractmethod
    def paste_all_data(self):
        pass
    
class IDBModels(ABC):
    @abstractmethod
    def create_tables(self):
        pass