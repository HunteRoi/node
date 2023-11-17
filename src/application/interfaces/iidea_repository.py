from abc import ABC, abstractmethod
from src.domain.entities.idea import Idea


class IIdeaRepository(ABC):
    """Interface for idea repository"""

    @abstractmethod
    def initialize_if_not_exists(self, target_database: str):
        """Initialize the requirements"""

    @abstractmethod
    def add_idea_to_community(self, community_id: str, idea: Idea) -> None:
        """Add an idea to a specific community"""

    @abstractmethod
    def get_ideas_by_community(self, community_id: str) -> list[Idea]:
        """Get ideas by community"""
