from abc import ABC, abstractmethod

from src.domain.entities.member import Member


class IMemberRepository(ABC):
    """Interface for the member repository class"""

    @abstractmethod
    def add_member_to_community(self, community_id: str, member: Member) -> None:
        """Add a member to a specific community"""

    @abstractmethod
    def get_member_for_community(self, community_id: str, member_auth_key: str) -> Member | None:
        """Get a member of a specific community"""
