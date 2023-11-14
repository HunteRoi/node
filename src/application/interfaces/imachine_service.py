from abc import ABC, abstractmethod


class IMachineService(ABC):
    """Interface for ID generator service"""

    @abstractmethod
    def get_ip_address(self) -> str:
        """Gets the machine's IP address"""

    @abstractmethod
    def get_auth_key(self, community_id: int | None) -> str:
        """Gets the machine's authentication key"""
