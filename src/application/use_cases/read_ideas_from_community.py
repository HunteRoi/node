from src.application.interfaces.iread_ideas_from_community import IReadIdeasFromCommunity
from src.application.interfaces.iidea_repository import IIdeaRepository
from src.domain.entities.idea import Idea


class ReadIdeasFromCommunity(IReadIdeasFromCommunity):
    """Use case to read ideas from community."""

    def __init__(self, idea_repository: IIdeaRepository):
        self.idea_repository = idea_repository

    def execute(self, community_id: int) -> list[Idea]:
        return self.idea_repository.get_ideas_by_community(community_id)
