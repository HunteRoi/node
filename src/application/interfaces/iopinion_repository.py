from abc import ABC, abstractmethod
from src.domain.entities.opinion import Opinion


class IOpinionRepository(ABC):
    """Interface for opinion repository"""

    @abstractmethod
    def initialize_if_not_exists(self, target_database: str):
        """Initialize the requirements"""

    @abstractmethod
    def add_opinion_to_community(self, community_id: str, opinion: Opinion) -> None:
        """Add an opinion to a specific community"""

    @abstractmethod
    def get_opinions_by_parent(self, community_id: str, parent_id: int) -> list[Opinion]:
        """Get opinions by parent"""
