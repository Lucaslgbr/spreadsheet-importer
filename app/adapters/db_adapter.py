# app/adapters/db_adapter.py

from typing import Any, Dict
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.ports.database_port import DatabasePort
from app.core.entities.spreadsheet import Spreadsheet
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/spreadsheet_db")

Base = declarative_base()

class SpreadsheetModel(Base):
    __tablename__ = "spreadsheets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    data = Column(JSON, nullable=False)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class DatabaseAdapter(DatabasePort):
    def __init__(self):
        Base.metadata.create_all(bind=engine)

    def save_spreadsheet(self, spreadsheet: Spreadsheet, user_id: str):
        db = SessionLocal()
        try:
            db_spreadsheet = SpreadsheetModel(user_id=user_id, data=spreadsheet.data)
            db.add(db_spreadsheet)
            db.commit()
            db.refresh(db_spreadsheet)
        finally:
            db.close()
