from abc import ABC, abstractmethod

class DatabasePort(ABC):

    def save_data(self, data: list):
        pass