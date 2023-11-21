from abc import ABC, abstractmethod


class IServerSocket(ABC):
    """interface server socket class"""

    @abstractmethod
    def run(self):
        """Run server"""

    @abstractmethod
    def stop(self):
        """Stop server"""
