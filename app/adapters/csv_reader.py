import csv
from typing import List
from core.ports.csv_port import CsvPort

class CsvReader(CsvPort):
    def read_csv(self, file_path: str) -> List[dict]:
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            return [row for row in csv_reader]