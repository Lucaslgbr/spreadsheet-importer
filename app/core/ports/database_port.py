from abc import ABC, abstractmethod

class DatabasePort(ABC):
    @abstractmethod
    def save_data(self, data: list):
        pass