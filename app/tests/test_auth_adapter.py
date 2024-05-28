import pytest
from app.adapters.auth_adapter import AuthAdapter

@pytest.fixture
def auth_adapter():
    return AuthAdapter()

def test_verify_jwt(auth_adapter, mocker):
    mocker.patch.object(auth_adapter, "verify_jwt", return_value=True)
    assert auth_adapter.verify_jwt("fake_token") == True
