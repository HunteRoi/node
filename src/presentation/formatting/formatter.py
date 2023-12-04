from src.presentation.formatting.message_dataclass import MessageDataclass
from src.presentation.formatting.message_dataclass import MessageHeader
from src.application.exceptions.message_error import MessageError


class Formatter:
    """The formatter class of message to send and receive"""

    def format_message(self, message: MessageDataclass) -> str:
        """Method to format a message object to message string"""
        if message.header in MessageHeader.__members__:
            return f"{message.header}|{message.content}"
        else:
            raise MessageError("Invalid message header")

    def parse(self, formated_message: str) -> MessageDataclass:
        """Method to parse the message string to a message object"""
        header, content = formated_message.split("|")
        return MessageDataclass(header, content)
