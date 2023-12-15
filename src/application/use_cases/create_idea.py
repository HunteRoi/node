from datetime import datetime

from src.application.interfaces.icreate_idea import ICreateIdea
from src.application.interfaces.iid_generator_service import IIdGeneratorService
from src.application.interfaces.iidea_repository import IIdeaRepository
from src.application.interfaces.imachine_service import IMachineService
from src.domain.entities.idea import Idea


class CreateIdea(ICreateIdea):
    """Create an idea."""

    def __init__(
        self,
        machine_service: IMachineService,
        id_generator_service: IIdGeneratorService,
        idea_repository: IIdeaRepository,
    ):
        self.machine_service = machine_service
        self.id_generator_service = id_generator_service
        self.idea_repository = idea_repository

    def execute(self, community_id: str, content: str) -> Idea:
        """Create an idea."""
        author = self.machine_service.get_current_user(community_id)
        creation_date = datetime.now()

        idea = Idea(
            self.id_generator_service.generate(), content, author, creation_date
        )
        self.idea_repository.add_idea_to_community(community_id, idea)

        return idea
