from datetime import datetime
from abc import ABC

from src.domain.entities.member import Member


class Message(ABC):
    """Represents the base for the opinion and idea entities."""

    def __init__(
        self,
        identifier: str,
        content: str,
        author: Member,
        creation_date: datetime = datetime.now(),
    ):
        self.identifier = identifier
        self.content = content
        self.author = author
        self.creation_date = creation_date
