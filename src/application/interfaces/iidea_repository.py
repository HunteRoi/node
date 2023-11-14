from abc import ABC, abstractmethod
from src.domain.entities.idea import Idea


class IIdeaRepository(ABC):
    """Interface for idea repository"""

    @abstractmethod
    def add_idea_to_community(self, community_id: str, idea: Idea) -> None:
        """Add an idea to a specific community"""

    @abstractmethod
    def get_ideas_by_community(self, community_id: str) -> list[Idea]:
        """Get ideas by community"""
