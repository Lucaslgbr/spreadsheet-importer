import requests
import logging
import os
from core.ports.auth_port import AuthPort
from fastapi import HTTPException

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Usar o nome do serviço Docker como endereço do serviço de autenticação
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth:8000/validate-token")

class AuthAdapter(AuthPort):
    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            logger.info(f"Verifying JWT token with authentication service at {AUTH_SERVICE_URL}")
            response = requests.post(AUTH_SERVICE_URL, headers={"Authorization": f"Bearer {jwtoken}"})
            logger.info(f"Received response from authentication service: {response.status_code} {response.text}")
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Error connecting to authentication service: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Authentication service connection error: {str(e)}")
        return False