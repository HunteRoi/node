class ParentNotFoundError(Exception):
    """Raised when a parent is not found"""

    def __init__(self, message="Parent not found"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"
