from datetime import datetime


class Member:
    """Member class"""

    def __init__(self,
                 authentication_key: str,
                 ip_address: str,
                 creation_date=datetime.now(),
                 last_connection_date=datetime.now()):
        self.authentication_key = authentication_key
        self.ip_address = ip_address
        self.creation_date = creation_date
        self.last_connection_date = last_connection_date

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Member):
            return False
        return self.authentication_key == __value.authentication_key
