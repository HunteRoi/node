from datetime import datetime

from src.domain.common.message import Message
from src.domain.entities.member import Member
from src.domain.entities.idea import Idea  # pylint: disable=unused-import


class Opinion(Message):
    """Opinion class"""

    def __init__(
        self,
        identifier: str,
        content: str,
        author: Member,
        creation_date: datetime,
        parent: "Opinion | Idea",
    ):
        super().__init__(identifier, content, author, creation_date)
        self.parent = parent

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Opinion):
            return False
        return self.identifier == __value.identifier

    def to_str(self) -> str:
        """Returns a string representation of the idea."""
        author_id = self.author.authentication_key
        return f"{self.identifier},{self.content},{author_id},{self.creation_date.isoformat()},{self.parent.identifier}"
