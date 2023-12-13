from abc import ABC, abstractmethod

from src.domain.entities.idea import Idea


class ICreateIdea(ABC):
    """Represents the use case to create an idea."""

    @abstractmethod
    def execute(self, community_id: str, content: str) -> Idea:
        """Creates an idea."""
