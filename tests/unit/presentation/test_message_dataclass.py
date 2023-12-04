import pytest
from src.presentation.formatting.message_dataclass import (
    MessageDataclass,
    MessageHeader,
)


class TestMessageDataclass:
    """The test message dataclass"""

    @pytest.mark.parametrize(
        "header",
        [
            MessageHeader.INVITATION,
            MessageHeader.AUTH_KEY,
            MessageHeader.PUBLIC_KEY,
            MessageHeader.CONFIRM_ADD_MEMBER,
            MessageHeader.REFUSED_ADD_MEMBER,
        ],
    )
    def test_message_dataclass_creation(self, header: MessageHeader):
        """Test message dataclass creation"""

        content = "content"

        message_data = MessageDataclass(header, content)

        assert message_data.header == header
        assert message_data.content == content
