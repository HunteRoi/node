from abc import ABC, abstractmethod

from src.domain.entities.opinion import Opinion


class IReadOpinions(ABC):
    """Interface to read opinions of an idea or opinion"""

    @abstractmethod
    def execute(self, community_id: int, idea_or_opinion_id: int) -> list[Opinion]:
        """Read opinions of an idea or opinion"""
