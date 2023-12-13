from abc import ABC, abstractmethod

from src.domain.entities.member import Member


class IMachineService(ABC):
    """Interface for ID generator service"""

    @abstractmethod
    def get_ip_address(self) -> str:
        """Gets the machine's IP address"""

    @abstractmethod
    def get_auth_key(self, community_id: int | None = None) -> str:
        """Gets the machine's authentication key"""

    @abstractmethod
    def get_port(self) -> int:
        """Gets the machine's port"""

    @abstractmethod
    def get_asymetric_key_pair(self) -> tuple[str, str]:
        """Gets the machine's asymetric key pair"""

    @abstractmethod
    def get_current_user(self, community_id: str | None = None) -> Member:
        """Gets the machine's current user"""
