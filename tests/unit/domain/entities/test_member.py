from datetime import datetime

from src.domain.entities.member import Member


class TestMember:
    """Test Member class"""

    def test_init_member(self):
        """Test init member"""
        member = Member("abc", "127.0.0.1")

        assert member is not None

    def test_auth_key_member(self):
        """Test auth key member"""
        auth_key = "abc"
        member = Member(auth_key, "127.0.0.1")

        assert member.authentication_key == auth_key

    def test_ip_member(self):
        """Test ip member"""
        auth_key = "abc"
        ip_address = "127.0.0.1"
        member = Member(auth_key, ip_address)

        assert member.ip_address == ip_address

    def test_creation_date_member(self):
        """Test last connection date member"""
        date_time = datetime.now()

        member = Member("abc", "127.0.0.1", date_time)

        assert member.creation_date == date_time

    def test_last_connection_date_member(self):
        """Test last connection date member"""
        date_time = datetime.now()

        member = Member("abc", "127.0.0.1", last_connection_date=date_time)

        assert member.last_connection_date == date_time

    def test_member_compared_to_another(self):
        """Validate that a member can be compared to another member"""
        member = Member("abc", "127.0.0.1")
        member2 = Member("abc", "127.0.0.1")

        assert member == member2

    def test_member_compared_to_another_with_different_auth_key(self):
        """Validate that a member can be compared to another member 
        with a different authentification key"""
        member = Member("abc", "127.0.0.1")
        member2 = Member("def", "127.0.0.1")

        assert member != member2

    def test_member_compared_to_another_object(self):
        """Validate that a member can be compared to another object"""
        member = Member("abc", "127.0.0.1")
        member2 = "abc"

        assert member != member2
