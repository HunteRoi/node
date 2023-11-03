from datetime import datetime
from src.domain.entities.member import Member


class Community:
    """A community is a group of people who share a common interest."""

    def __init__(self, identifier: str,
                 name: str,
                 description: str,
                 creation_date: datetime = datetime.now()):
        self.identifier = identifier
        self.name = name
        self.description = description
        self.creation_date = creation_date
        self.members = {}

    def add_member(self, member: Member):
        """Add a member to the community."""
        self.members[member.ip_address] = member

    def remove_member(self, member: Member):
        """Remove a member from the community."""
        self.members.pop(member.ip_address)

    def remove_member_based_on(self, ip_address: str):
        """Remove a member from the community based on their IP address."""
        self.members.pop(ip_address)
