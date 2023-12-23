from abc import ABC, abstractmethod


class ICreateOpinion(ABC):
    """Represents the use case to create an opinion."""

    @abstractmethod
    def execute(self, community_id: str, idea_or_opinion_id: str, content: str):
        """Creates an opinion."""
