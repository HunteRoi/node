from abc import ABC, abstractmethod

from src.domain.entities.community import Community


class IReadCommunities(ABC):
    """Interface for read communities"""

    @abstractmethod
    def execute(self) -> list[Community]:
        """Read communities"""
