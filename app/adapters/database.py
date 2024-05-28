from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
from app.core.ports.database_port import DatabasePort
from app.core.entities.spreadsheet import Spreadsheet
import os
import json

# Use the DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/spreadsheet_db")

class Database(DatabasePort):
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.metadata = MetaData()

        # Define a única tabela para todos os modelos de planilhas
        self.spreadsheets_table = Table('spreadsheets', self.metadata,
                                        Column('id', Integer, primary_key=True, index=True),
                                        Column('user_id', String, nullable=False),
                                        Column('data', String, nullable=False))  # Coluna para armazenar JSON

        self.metadata.create_all(self.engine)

    def save_spreadsheet(self, spreadsheet: Spreadsheet, user_id: str):
        session = self.SessionLocal()
        table = self.spreadsheets_table
        try:
            json_data = json.dumps(spreadsheet.data)  # Converte os dados em JSON
            insert_stmt = table.insert().values(user_id=user_id, data=json_data)
            session.execute(insert_stmt)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
