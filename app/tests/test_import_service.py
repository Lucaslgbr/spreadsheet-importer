import pytest
from app.core.services.import_service import ImportService
from app.adapters.database import Database
from app.core.entities.spreadsheet import Spreadsheet

from sqlalchemy.sql import text


@pytest.fixture
def db_adapter():
    return Database()

@pytest.fixture
def import_service(db_adapter):
    return ImportService(db_adapter=db_adapter)

async def test_import_spreadsheet(import_service, mocker):
    file_path = "/tmp/test_file.csv"
    mocker.patch("builtins.open", mocker.mock_open(read_data="Data;descrição;referencia;nota fiscal;entrada;saida\n01/01/2023;Compra;123;456;100.00;0.00\n"))
    mocker.patch("os.remove")

    await import_service.import_spreadsheet(file_path, "test_user", "test_file.csv")
    db = import_service.db_adapter
    session = db.SessionLocal()
    result = session.execute(text("SELECT * FROM spreadsheets")).fetchall()
    assert len(result) == 1
    assert result[0]["user_id"] == "test_user"
    assert result[0]["file_name"] == "test_file.csv"
