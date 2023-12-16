from src.domain.common.message import Message


class Idea(Message):
    """Idea class"""

    # This class is a subclass of Message, so it inherits all the attributes and methods of Message.
    # The __init__ method of this class is overriding the __init__ method of Message.

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Idea):
            return False
        return self.identifier == __value.identifier

    def to_str(self) -> str:
        """Returns a string representation of the idea."""
        author_id = self.author.authentication_key
        return f"{self.identifier},{self.content},{author_id},{self.creation_date.isoformat()}"
