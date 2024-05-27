import csv
from app.core.ports.csv_port import CsvPort
from app.core.entities.spreadsheet import Spreadsheet

class CsvReaderModel1(CsvPort):
    def read(self, file_path: str) -> Spreadsheet:
        data = []
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append({
                    "Data": row["Data"],
                    "Descrição": row["descrição"],
                    "Referência": row["referencia"],
                    "Nota Fiscal": row["nota fiscal"],
                    "Entrada": row["entrada"],
                    "Saída": row["saida"]
                })
        return Spreadsheet(data=data)
