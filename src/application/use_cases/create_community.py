from src.application.interfaces.icreate_community import ICreateCommunity
from src.application.interfaces.icommunity_repository import ICommunityRepository
from src.application.interfaces.iid_generator_service import IIdGeneratorService
from src.domain.entities.community import Community


class CreateCommunity(ICreateCommunity):
    """Class to create a community"""

    def __init__(self, repository: ICommunityRepository, id_generator_service: IIdGeneratorService):
        self.repository = repository
        self.id_generator_service = id_generator_service

    def execute(self, name: str, description: str):
        """Create a community"""
        community_id = self.id_generator_service.generate()
        community = Community(community_id, name, description)
        self.repository.add_community(community)
