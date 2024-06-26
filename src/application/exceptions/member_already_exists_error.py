class MemberAlreadyExistsError(Exception):
    """
    Exception raised when attempting to create a member that already exists.
    """

    def __init__(self, inner_error: Exception):
        super().__init__()
        self.inner_error = inner_error

    def __str__(self):
        return f"Member already exists: {self.inner_error}"
