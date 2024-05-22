from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Usar o nome do serviço Docker como endereço do serviço de autenticação
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth:8000/validate-token")

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

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
