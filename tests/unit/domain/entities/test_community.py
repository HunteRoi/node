from datetime import datetime

from src.domain.entities.community import Community
from src.domain.entities.member import Member


class TestCommunity:
    """Test Community class"""

    def test_init(self):
        """Validates the constructor of Community initializes the object"""
        community = Community("1", "name", "desc")

        assert community is not None

    def test_id_attribute(self):
        """Validates that a community created with a specified ID has that ID"""
        id_community = "1"

        community = Community(id_community, "name", "desc")

        assert community.identifier == id_community

    def test_name_attribute(self):
        """Validates that a community created with a specified name has that name"""
        name_community = "name"

        community = Community("1", name_community, "desc")

        assert community.name == name_community

    def test_description_attribute(self):
        """Validates that a community created with a specified description has 
        that description"""
        desc_community = "desc"

        community = Community("1", "name", desc_community)

        assert community.description == desc_community

    def test_creation_date_attribute(self):
        """Validates that a community created with a specified creation date has 
        that creation date"""
        creation_date_community = datetime.now()

        community = Community("1", "name", "desc", creation_date_community)

        assert community.creation_date == creation_date_community

    def test_members(self):
        """Validates that a community has no members when created"""
        community = Community("1", "name", "desc")

        assert community.members is not None

    def test_add_member(self):
        """Validates that a member can be added to the community"""
        community = Community("1", "name", "desc")
        member = Member("127.0.0.1", datetime.now())

        community.add_member(member)

        assert member.ip_address in community.members

    def test_remove_member(self):
        """Validate that a member can be removed from the community"""
        community = Community("1", "name", "desc")
        member = Member("127.0.0.1", datetime.now())

        community.add_member(member)
        assert len(community.members) == 1

        community.remove_member(member)
        assert len(community.members) == 0

    def test_remove_member_specific(self):
        """Validate that a specific member can be removed from the community"""
        community = Community("1", "name", "desc")
        member = Member("127.0.0.1", datetime.now())
        member2 = Member("127.0.0.2", datetime.now())

        community.add_member(member)
        community.add_member(member2)

        assert len(community.members) == 2

        community.remove_member(member2)

        assert len(community.members) == 1
        assert member.ip_address in community.members

    def test_remove_member_based_on_ip(self):
        """Validate that a member can be removed from the community if the IP is the same"""
        community = Community("1", "name", "desc")
        member = Member("127.0.0.1", datetime.now())

        community.add_member(member)
        assert len(community.members) == 1

        community.remove_member_based_on(member.ip_address)

        assert len(community.members) == 0
