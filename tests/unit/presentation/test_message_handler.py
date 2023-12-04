from unittest import mock
import pytest

from src.presentation.handler.message_handler import MessageHandler
from src.presentation.formatting.message_dataclass import (
    MessageDataclass,
    MessageHeader,
)
from src.application.exceptions.message_error import MessageError


class TestMessageHandler:
    """Test class for MessageHandler"""

    @pytest.fixture(
        params=[
            MessageHeader.INVITATION,
        ]
    )
    def message_data(self, request):
        """Fixture to create a MessageDataclass with different MessageHeader."""
        header = request.param
        content = "content"
        return MessageDataclass(header=header, content=content)

    @mock.patch("src.application.interfaces.iread_communities.IReadCommunities")
    def test_handle_message(self, mock_usecase, message_data):
        """Test method for handle_message with different MessageHeader."""
        message_handler = MessageHandler(mock_usecase)

        message_handler.handle_message(message_data)

        mock_usecase.execute.assert_called_once_with(message_data.content)

    @mock.patch("src.application.interfaces.iread_communities.IReadCommunities")
    def test_invalid_handler_message(self, mock_usecase):
        """Test method for handle_message with invalid MessageDataclass."""
        invalid_message_data = MessageDataclass(
            header="INVALID_HEADER", content="content"
        )
        message_handler = MessageHandler(mock_usecase)

        with pytest.raises(MessageError):
            message_handler.handle_message(invalid_message_data)
