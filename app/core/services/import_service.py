from app.core.ports.csv_port import CsvPort
from app.core.ports.database_port import DatabasePort
from app.core.entities.spreadsheet import Spreadsheet

class ImportService:
    def __init__(self, csv_adapter: CsvPort, db_adapter: DatabasePort):
        self.csv_adapter = csv_adapter
        self.db_adapter = db_adapter

    def import_spreadsheet(self, file_path: str):
        spreadsheet = self.csv_adapter.read(file_path)
        self.db_adapter.save_spreadsheet(spreadsheet)
