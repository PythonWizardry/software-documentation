from abc import ABC, abstractmethod

class IPresentation(ABC):
    @abstractmethod
    def display(self, data):
        pass

