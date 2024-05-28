from fastapi.testclient import TestClient
from main import app
from app.adapters.auth_adapter import AuthAdapter
from app.core.middleware.auth_middleware import JWTBearer
import pytest
from unittest.mock import patch, MagicMock


client = TestClient(app)

@pytest.fixture
def test_file():
    return "app/tests/test_file.csv"

@pytest.fixture
def auth_adapter(mocker):
    adapter = AuthAdapter()
    mocker.patch.object(adapter, "verify_jwt", return_value=True)
    return adapter

def test_upload_file(test_file, auth_adapter):
    # Criando um mock do JWTBearer
    mock_jwt_bearer = JWTBearer(auth_adapter)
    mock_jwt_bearer.__call__ = MagicMock(return_value="fake_jwt_token")

    with patch("app.adapters.auth_adapter", auth_adapter):
        with patch("app.core.middleware.auth_middleware", return_value=mock_jwt_bearer):
            with open(test_file, "rb") as f:
                response = client.post(
                    "api/v1/uploadfile/",
                    files={"file": f},
                    data={"name": "test_name", "user_id": "test_user"},
                    headers={"Authorization": "Bearer fake_jwt_token"}
                )
    assert response.status_code == 403
def test_get_list(mocker):
    mocker.patch.object(AuthAdapter, "verify_jwt", return_value=True)
    response = client.get("api/v1/get_list/", params={"user_id": "test_user"})
    assert response.status_code == 403
