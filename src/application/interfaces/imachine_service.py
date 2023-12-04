from abc import ABC, abstractmethod


class IMachineService(ABC):
    """Interface for ID generator service"""

    @abstractmethod
    def get_ip_address(self) -> str:
        """Gets the machine's IP address"""

    @abstractmethod
    def get_auth_key(self, community_id: int | None) -> str:
        """Gets the machine's authentication key"""

    @abstractmethod
    def get_port(self) -> int:
        """Gets the machine's port"""

    @abstractmethod
    def get_asymetric_key_pair(self) -> tuple[str, str]:
        """Gets the machine's asymetric key pair"""
