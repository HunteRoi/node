from abc import ABC, abstractmethod


class ICreateCommunity(ABC):
    """Represents the use case for creating a community."""

    @abstractmethod
    def execute(self, name: str, description: str) -> str:
        """Create a community"""
