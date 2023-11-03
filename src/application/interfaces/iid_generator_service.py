from abc import ABC, abstractmethod


class IIdGeneratorService(ABC):
    """Interface for ID generator service"""

    @abstractmethod
    def generate(self) -> str:
        """Generates an ID"""
