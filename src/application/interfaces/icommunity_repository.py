from abc import ABC, abstractmethod

from src.domain.entities.community import Community


class ICommunityRepository(ABC):
    """Interface for the repository class"""

    @abstractmethod
    def initialize_if_not_exists(self, target_database: str):
        """Initialize the requirements"""

    @abstractmethod
    def add_community(self, community: Community, member_auth_key: str) -> None:
        """Add a community to the repository"""

    @abstractmethod
    def get_community(self, community_id: str) -> None | Community:
        """Get a community from the repository"""

    @abstractmethod
    def get_communities(self) -> list[Community]:
        """Get the communities from the repository"""

    @abstractmethod
    def get_authentication_key_for_community(self, community_id: str) -> str:
        """Get the authentication key of the current member of the community"""
