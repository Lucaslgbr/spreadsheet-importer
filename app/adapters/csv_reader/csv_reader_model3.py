import csv
from app.core.ports.csv_port import CsvPort
from app.core.entities.spreadsheet import Spreadsheet

class CsvReaderModel3(CsvPort):
    def read(self, file_path: str) -> Spreadsheet:
        data = []
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append({
                    "Data": row["Data"],
                    "Descrição": row["descrição"],
                    "Documento": row["documento"],
                    "Crédito": row["crédito"],
                    "Débito": row["débito"],
                    "Saldo": row["saldo"]
                })