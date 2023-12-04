import pytest

from src.presentation.formatting.message_dataclass import (
    MessageDataclass,
    MessageHeader,
)
from src.presentation.formatting.formatter import Formatter
from src.application.exceptions.message_error import MessageError


class TestFormatter:
    """the test formatter class of message"""

    @pytest.fixture(
        params=[
            MessageHeader.INVITATION,
            MessageHeader.AUTH_KEY,
            MessageHeader.PUBLIC_KEY,
            MessageHeader.CONFIRM_ADD_MEMBER,
            MessageHeader.REFUSED_ADD_MEMBER,
        ]
    )
    def message_data(self, request):
        """Fixture to create a MessageDataclass with different MessageHeader."""
        header = request.param
        content = "content"
        return MessageDataclass(header=header, content=content)

    @pytest.fixture
    def formatter(self):
        """Fixture to create a default Formatter for testing."""
        return Formatter()

    def test_format_message(self, formatter, message_data):
        """Test method to format object to str with different message headers."""
        formated_message = formatter.format_message(message_data)
        expected_message = f"{message_data.header}|{message_data.content}"
        assert formated_message == expected_message

    def test_invalid_format_message(self, formatter):
        """Test metthod to check invalid message header formatting"""
        invalid_message_data = MessageDataclass(
            header="INVALID_HEADER", content="content"
        )
        with pytest.raises(MessageError):
            formatter.format_message(invalid_message_data)

    def test_parse_invitation_string_message(self):
        """test methode to parse str to object invitation message"""
        formated_data = "INVITATION|content"
        formatter = Formatter()
        parse_message = formatter.parse(formated_data)

        assert parse_message.header == MessageHeader.INVITATION
        assert parse_message.content == "content"
