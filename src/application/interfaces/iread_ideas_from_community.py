from abc import ABC, abstractmethod

from src.domain.entities.idea import Idea


class IReadIdeasFromCommunity(ABC):
    """Interface for read ideas from community"""

    @abstractmethod
    def execute(self, community_id: int) -> list[Idea]:
        """Read ideas from community"""
