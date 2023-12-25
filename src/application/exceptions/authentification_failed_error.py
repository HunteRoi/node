class AuthentificationFailedError(Exception):
    """
    Exception raised when member authentification failed.
    """

    def __init__(self, inner_error: Exception):
        super().__init__()
        self.inner_error = inner_error

    def __str__(self):
        return f"Authentification failed: {self.inner_error}"
