from abc import ABC, abstractmethod

class YoloInterface(ABC):
    @abstractmethod
    def detectObjects(self, image_path: str) -> list:
        pass

    @abstractmethod
    def getConfidenceScore(self, detection: dict) -> float:
        pass