import csv
from app.core.ports.csv_port import CsvPort
from app.core.entities.spreadsheet import Spreadsheet

class CsvReaderModel2(CsvPort):
    def read(self, file_path: str) -> Spreadsheet:
        data = []
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                data.append({
                    "Data": row["Data"],
                    "Descrição": row["descrição"],
                    "Valor": row["valor"],
                    "Descricao": row["descricao"]
                })
        return Spreadsheet(data=data)
