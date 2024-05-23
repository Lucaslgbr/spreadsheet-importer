from core.ports.csv_port import CsvPort
from core.ports.database_port import DatabasePort
from core.entities.spreadsheet import Spreadsheet

class ImportService:
    def __init__(self, csv_port: CsvPort, db_port: DatabasePort):
        self.csv_port = csv_port
        self.db_port = db_port

    def import_spreadsheet(self, file_path: str):
        data = self.csv_port.read_csv(file_path)
        spreadsheet = Spreadsheet(data)
        self.db_port.save_data(spreadsheet.data)