from datetime import datetime

from src.domain.entities.member import Member


class TestMember:
    """Test Member class"""

    def test_init_member(self):
        """Test init member"""
        member = Member("127.0.0.1", datetime.now())

        assert member is not None

    def test_ip_member(self):
        """Test ip member"""
        ip_address = "127.0.0.1"
        member = Member(ip_address, datetime.now())

        assert member.ip_address == ip_address

    def test_last_connection_date_member(self):
        """Test last connection date member"""
        date_time = datetime.now()

        member = Member("127.0.0.1", date_time)

        assert member.last_connection_date == date_time
