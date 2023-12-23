from src.application.interfaces.iread_opinions import IReadOpinions
from src.application.interfaces.iopinion_repository import IOpinionRepository
from src.domain.entities.opinion import Opinion


class ReadOpinions(IReadOpinions):
    """Use case to read opinions from idea of opinion."""

    def __init__(self, opinion_repository: IOpinionRepository):
        self.opinion_repository = opinion_repository

    def execute(self, community_id: str, idea_or_opinion_id: str) -> list[Opinion]:
        return self.opinion_repository.get_opinions_by_parent(
            community_id, idea_or_opinion_id
        )
