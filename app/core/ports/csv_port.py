from abc import ABC, abstractmethod
from typing import List

class CsvPort(ABC):

    def read_csv(self, file_path: str) -> List[dict]:
        pass