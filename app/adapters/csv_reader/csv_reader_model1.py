from app.core.ports.csv_port import CsvPort
from app.core.entities.spreadsheet import Spreadsheet
import csv
class CsvReaderModel1(CsvPort):
    def read_csv(self, file_path: str) -> Spreadsheet:
        data = []
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                data.append({
                    "Data": row.get("Data"),
                    "Descrição": row.get("descrição"),
                    "Referência": row.get("referencia"),
                    "Nota Fiscal": row.get("nota fiscal"),
                    "Entrada": row.get("entrada"),
                    "Saída": row.get("saida")
                })
        return Spreadsheet(data=data)