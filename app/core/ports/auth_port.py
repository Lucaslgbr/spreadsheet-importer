from abc import ABC, abstractmethod

class AuthPort(ABC):
    @abstractmethod
    def verify_jwt(self, jwtoken: str) -> bool:
        pass