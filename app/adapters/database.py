from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, Table
from sqlalchemy.orm import sessionmaker
from app.core.ports.database_port import DatabasePort
from app.core.entities.spreadsheet import Spreadsheet
import os

# Use the DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/spreadsheet_db")

class Database(DatabasePort):
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.metadata = MetaData()

        self.spreadsheets_table = Table('spreadsheets', self.metadata,
                                        Column('id', Integer, primary_key=True, index=True),
                                        Column('user_id', String, nullable=False),
                                        Column('model_type', Integer, nullable=False),
                                        Column('Data', String, nullable=True),
                                        Column('Descrição', String, nullable=True),
                                        Column('Referência', String, nullable=True),
                                        Column('Nota_Fiscal', String, nullable=True),
                                        Column('Entrada', Float, nullable=True),
                                        Column('Saída', Float, nullable=True),
                                        Column('Valor', Float, nullable=True),
                                        Column('Documento', String, nullable=True),
                                        Column('Crédito', Float, nullable=True),
                                        Column('Débito', Float, nullable=True),
                                        Column('Saldo', Float, nullable=True))

        self.metadata.create_all(self.engine)

    def save_spreadsheet(self, spreadsheet: Spreadsheet, model_type: int, user_id: str):
        session = self.SessionLocal()
        table = self.spreadsheets_table
        try:
            for row in spreadsheet.data:
                row['model_type'] = model_type
                row['user_id'] = user_id
                insert_stmt = table.insert().values(**row)
                session.execute(insert_stmt)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
