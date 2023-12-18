from datetime import datetime

from src.domain.entities.member import Member


class Community:
    """A community is a group of people who share a common interest."""

    def __init__(
        self,
        identifier: str,
        name: str,
        description: str,
        creation_date: datetime = datetime.now(),
    ):
        self.identifier = identifier
        self.name = name
        self.description = description
        self.creation_date = creation_date
        self.members = {}

    def add_member(self, member: Member):
        """Add a member to the community."""
        self.members[member.authentication_key] = member

    def remove_member(self, member: Member):
        """Remove a member from the community."""
        self.members.pop(member.authentication_key)

    def remove_member_based_on(self, authentication_key: str):
        """Remove a member from the community based on their authentication key."""
        self.members.pop(authentication_key)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Community):
            return False
        return self.identifier == __value.identifier

    def to_str(self) -> str:
        """Returns a string representation of the community."""
        return f"{self.identifier},{self.name},{self.description},{self.creation_date.isoformat()}"
