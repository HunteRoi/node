from typing import Any
from dataclasses import dataclass

from src.presentation.formatting.message_header import MessageHeader


@dataclass
class MessageDataclass:
    """The dataclass of all messages type"""

    header: MessageHeader
    content: Any
