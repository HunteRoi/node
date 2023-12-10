from abc import ABC, abstractmethod


class IAddMember(ABC):
    """interface add member class"""

    @abstractmethod
    def execute(self, community_id: str, ip_address: str, port: int) -> str:
        """methode execute add a member to a community"""
