class MessageError(Exception):
    """Exception raised for errors in the input message"""

    def __init__(self, inner_error: Exception):
        super().__init__()
        self.inner_error = inner_error
