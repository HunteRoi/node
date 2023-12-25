class CommunityAlreadyExistsError(Exception):
    """
    Exception raised when attempting to create a community that already exists.
    """

    def __init__(self, inner_error: Exception):
        super().__init__()
        self.inner_error = inner_error

    def __str__(self):
        return f"Community already exists: {self.inner_error}"
