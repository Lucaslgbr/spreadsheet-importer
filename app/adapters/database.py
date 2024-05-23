from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.ports.database_port import DatabasePort

DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class SpreadsheetRecord(Base):
    __tablename__ = "spreadsheet_records"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(String, index=True)

Base.metadata.create_all(bind=engine)

class Database(DatabasePort):
    def save_data(self, data: list):
        db = SessionLocal()
        try:
            for row in data:
                db_record = SpreadsheetRecord(data=str(row))
                db.add(db_record)
            db.commit()
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()