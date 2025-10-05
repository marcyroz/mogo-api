from abc import ABC, abstractmethod

class AuthInterface(ABC):
    @abstractmethod
    def authenticateUser(self, username: str, password: str) -> dict:
        pass

    @abstractmethod
    def generateToken(self, user_id: int) -> str:
        pass