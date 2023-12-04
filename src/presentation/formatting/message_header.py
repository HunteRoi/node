from enum import StrEnum


class MessageHeader(StrEnum):
    """The headers of message types"""

    INVITATION = "INVITATION"
    AUTH_KEY = "AUTH_KEY"
    PUBLIC_KEY = "PUBLIC_KEY"
    CONFIRM_ADD_MEMBER = "CONFIRM_ADD_MEMBER"
    REFUSED_ADD_MEMBER = "REFUSED_ADD_MEMBER"
