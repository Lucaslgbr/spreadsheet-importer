import csv
from app.core.ports.csv_port import CsvPort
from app.core.entities.spreadsheet import Spreadsheet

class CsvReaderModel3(CsvPort):
    def read_csv(self, file_path: str) -> Spreadsheet:
        data = []
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                data.append({
                    "Data": row.get("Data"),
                    "Descrição": row.get("descrição"),
                    "Documento": row.get("documento"),
                    "Crédito": row.get("crédito"),
                    "Débito": row.get("débito"),
                    "Saldo": row.get("saldo")
                })
        return Spreadsheet(data=data)
    