from datetime import datetime
import pytest

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
        member = Member("abc", "127.0.0.1", datetime.now())

        community.add_member(member)

        assert member.authentication_key in community.members

    def test_remove_member(self):
        """Validate that a member can be removed from the community"""
        community = Community("1", "name", "desc")
        member = Member("abc", "127.0.0.1", datetime.now())

        community.add_member(member)
        assert len(community.members) == 1

        community.remove_member(member)
        assert len(community.members) == 0

    def test_remove_member_specific(self):
        """Validate that a specific member can be removed from the community"""
        community = Community("1", "name", "desc")
        member = Member("abc", "127.0.0.1", datetime.now())
        member2 = Member("def", "127.0.0.1", datetime.now())

        community.add_member(member)
        community.add_member(member2)

        assert len(community.members) == 2

        community.remove_member(member2)

        assert len(community.members) == 1
        assert member.authentication_key in community.members

    def test_remove_member_based_on_auth_key(self):
        """Validate that a member can be removed from the community
        if the authentication key is the same"""
        community = Community("1", "name", "desc")
        member = Member("abc", "127.0.0.1", datetime.now())

        community.add_member(member)
        assert len(community.members) == 1

        community.remove_member_based_on(member.authentication_key)

        assert len(community.members) == 0

    def test_community_compared_to_another(self):
        """Validate that a community can be compared to another community"""
        community = Community("1", "name", "desc")
        community2 = Community("1", "name", "desc")

        assert community == community2

    def test_community_compared_to_another_with_different_id(self):
        """Validate that a community can be compared to another community
        with a different ID"""
        community = Community("1", "name", "desc")
        community2 = Community("2", "name", "desc")

        assert community != community2

    def test_community_compared_to_another_object(self):
        """Validate that a community can be compared to another object"""
        community = Community("1", "name", "desc")
        community2 = "community"

        assert community != community2

    def test_community_to_string(self):
        """Validate that a community can be converted to a string"""
        creation_date = datetime.fromisoformat("2021-01-01T00:00:00")
        community = Community("1", "name", "desc", creation_date)

        assert community.to_str() == "1,name,desc,2021-01-01T00:00:00"

    def test_create_community_from_to_string(self):
        """Validate that a community can be created from a string"""
        creation_date = datetime.fromisoformat("2021-01-01T00:00:00")
        community = Community("1", "name", "desc", creation_date)
        community_str = "1,name,desc,2021-01-01T00:00:00"

        assert Community.from_str(community_str) == community

    def test_create_community_from_to_string_with_different_id(self):
        """Validate that a community can be created from a string
        with a different ID"""
        creation_date = datetime.fromisoformat("2021-01-01T00:00:00")
        community = Community("2", "name", "desc", creation_date)
        community_str = "1,name,desc,2021-01-01T00:00:00"

        assert Community.from_str(community_str) != community

    def test_create_community_from_to_string_with_empty_string(self):
        """Validate that a community can be created from an empty string"""
        community_str = ""

        with pytest.raises(ValueError):
            Community.from_str(community_str)

    def test_create_community_from_to_string_with_not_enough_values(self):
        """Validate that a community can be created from a string with not enough values"""
        community_str = "1,name,desc"

        with pytest.raises(ValueError):
            Community.from_str(community_str)

    def test_create_community_from_to_string_with_invalid_string(self):
        """Validate that a community can be created from a string with invalid string"""
        community_str = "1/name.desc,2021-01-01T00:00:00"

        with pytest.raises(ValueError):
            Community.from_str(community_str)

    def test_create_community_from_to_string_with_invalid_date(self):
        """Validate that a community can be created from a string with invalid date"""
        community_str = "1,name,desc,01/01/2021"

        with pytest.raises(ValueError):
            Community.from_str(community_str)
