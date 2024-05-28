from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
from app.core.ports.database_port import DatabasePort
from app.core.entities.spreadsheet import Spreadsheet
import os
import json

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/spreadsheet_db")

class Database(DatabasePort):
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.metadata = MetaData()

        self.spreadsheets_table = Table('spreadsheets', self.metadata,
                                        Column('id', Integer, primary_key=True, index=True),
                                        Column('user_id', String, nullable=False),
                                        Column('data', String, nullable=False),
                                        Column('file_name', String, nullable=False)) 
        self.metadata.create_all(self.engine)

    def save_spreadsheet(self, spreadsheet: Spreadsheet, user_id: str, file_name: str):
        session = self.SessionLocal()
        table = self.spreadsheets_table
        try:
            json_data = json.dumps(spreadsheet.data)
            insert_stmt = table.insert().values(user_id=user_id, data=json_data, file_name=file_name)
            session.execute(insert_stmt)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_spreadsheets_by_user(self, user_id: str):
        session = self.SessionLocal()
        table = self.spreadsheets_table
        try:
            select_stmt = table.select().where(table.c.user_id == user_id)
            result = session.execute(select_stmt).fetchall()
            spreadsheets = []
            for row in result:
                spreadsheets.append({
                    "file_name": row.file_name
                })
            return spreadsheets
        except Exception as e:
            raise e
        finally:
            session.close()
