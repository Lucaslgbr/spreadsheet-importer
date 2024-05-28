from app.core.ports.csv_port import CsvPort
from app.core.ports.database_port import DatabasePort
from app.core.entities.spreadsheet import Spreadsheet
from app.core.services.identify_csv_model import identify_csv_model
from app.adapters.rabbitmq_adapter import RabbitMQAdapter
import asyncio
class ImportService:
    def __init__(self, db_adapter: DatabasePort):
        self.db_adapter = db_adapter

    async def import_spreadsheet(self, file_path: str, user_id: str, file_name: str):
        await asyncio.sleep(5)  
        csv_adapter = identify_csv_model(file_path)  
        spreadsheet = csv_adapter.read_csv(file_path)
        self.db_adapter.save_spreadsheet(spreadsheet, user_id, file_name)
        message = {
            "email": user_id,
            "details": "Planilha processada",
            "user": user_id
        }
        rabbitmq_adapter = RabbitMQAdapter()
        rabbitmq_adapter.publish(message=message)
