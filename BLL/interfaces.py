from abc import ABC, abstractmethod

class ICourseService(ABC):

    @abstractmethod
    def create_tables(self):
        pass
    
    @abstractmethod
    def paste_data(self):
        pass