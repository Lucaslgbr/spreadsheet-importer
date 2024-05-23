from abc import ABC, abstractmethod

class MessageBrokerPort(ABC):
    @abstractmethod
    def publish(self, message: dict):
        pass