from abc import ABC, abstractmethod
from datetime import datetime


class IDatetimeService(ABC):
    """Interface for datetime service"""

    @abstractmethod
    def get_datetime(self) -> datetime:
        """Returns current time"""
