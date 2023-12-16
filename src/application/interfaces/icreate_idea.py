from abc import ABC, abstractmethod


class ICreateIdea(ABC):
    """Represents the use case to create an idea."""

    @abstractmethod
    def execute(self, community_id: str, content: str):
        """Creates an idea."""
