from abc import ABC, abstractmethod

from src.domain.entities.community import Community


class ICommunityRepository(ABC):
    """Interface for the repository class"""

    @abstractmethod
    def add_community(self, community: Community) -> None:
        """Add a community to the repository"""

    @abstractmethod
    def get_community(self, identifier: str) -> None | Community:
        """get community from db"""
