from abc import ABC, abstractmethod


class IClientSocket(ABC):
    """interface client socket class"""

    @abstractmethod
    def connect_to_server(self, ip_adress: str, port: int):
        """Connect to server"""

    @abstractmethod
    def send_message(
        self, message: str, ip_address: str | None = None, port: int | None = None
    ):
        """Send message"""

    @abstractmethod
    def receive_message(self) -> tuple[str, tuple[str, int]]:
        """Receive message"""

    @abstractmethod
    def close_connection(self):
        """Close connection"""
