from src.presentation.formatting.message_dataclass import MessageDataclass
from src.application.interfaces.iread_communities import (
    IReadCommunities,
)
from src.application.exceptions.message_error import MessageError
from src.presentation.formatting.message_header import MessageHeader


class MessageHandler:
    """The message handler class"""

    def __init__(self, usecase: IReadCommunities):
        self.usecase = usecase

    def handle_message(self, message: MessageDataclass):
        """Method to handle the message"""

        match message.header:
            case MessageHeader.INVITATION:
                self.usecase.execute(message.content)
            case _:
                raise MessageError("Invalid header in the message.")
