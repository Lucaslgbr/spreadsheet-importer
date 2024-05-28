import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends, HTTPException
from app.core.middleware.auth_middleware import JWTBearer
from app.adapters.auth_adapter import AuthAdapter

app = FastAPI()
auth_adapter = AuthAdapter()

def test_protected_route(mock_auth_service, mocker):
    mocker.patch.object(AuthAdapter, "verify_jwt", return_value=True)

@app.get("/protected")
async def protected_route(token: str = Depends(JWTBearer(auth_adapter))):
    return {"message": "Protected route"}

client = TestClient(app)

@pytest.fixture
def mock_auth_service(mocker):
    auth_service = mocker.Mock()
    auth_service.verify_jwt.return_value = True
    return auth_service
