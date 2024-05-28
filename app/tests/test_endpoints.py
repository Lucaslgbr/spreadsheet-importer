import pytest
from fastapi.testclient import TestClient
from main import app 
from app.core.services.import_service import ImportService
from app.adapters.database import Database
from app.adapters.auth_adapter import AuthAdapter

client = TestClient(app)

def test_import_spreadsheet():
    db_adapter = Database()
    import_service = ImportService(db_adapter=db_adapter)
    result = import_service.import_spreadsheet("test.csv", "user_id", "file_name")
    assert result == {"message": "Spreadsheet imported successfully."}

def test_import_spreadsheet_invalid_file():
    db_adapter = Database()
    import_service = ImportService(db_adapter=db_adapter)
    with pytest.raises(ValueError):
        import_service.import_spreadsheet("invalid_file.txt", "user_id", "file_name")

def test_authenticate_user():
    auth_adapter = AuthAdapter()
    result = auth_adapter.authenticate_user("username", "password")
    assert result == {"user_id": "123", "token": "your_token_here"}

def test_authenticate_user_invalid_credentials():
    auth_adapter = AuthAdapter()
    with pytest.raises(ValueError):
        auth_adapter.authenticate_user("invalid_username", "invalid_password")
