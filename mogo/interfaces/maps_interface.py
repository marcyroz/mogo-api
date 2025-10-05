from abc import ABC, abstractmethod

class MapsInterface(ABC):
    @abstractmethod
    def getRoute(self, origin: str, destination: str) -> dict:
        pass

    @abstractmethod
    def calculateDistance(self, origin: str, destination: str) -> float:
        pass