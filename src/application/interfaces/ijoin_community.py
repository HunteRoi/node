from abc import ABC, abstractmethod

from src.application.interfaces.iclient_socket import IClientSocket


class IJoinCommunity(ABC):
    """Join a community"""

    @abstractmethod
    def execute(self, client_socket: IClientSocket):
        """Execute the use case"""
