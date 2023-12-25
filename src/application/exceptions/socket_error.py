class SocketError(Exception):
    """
    Exception raised with a socket.
    """

    def __init__(self, inner_error: Exception):
        super().__init__()
        self.inner_error = inner_error

    def __str__(self):
        return f"Socket error: {self.inner_error}"
