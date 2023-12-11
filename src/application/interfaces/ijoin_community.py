from abc import ABC, abstractmethod


class IJoinCommunity(ABC):
    """Join a community"""

    @abstractmethod
    def execute(self):
        """Execute the use case"""
