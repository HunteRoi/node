from src.application.interfaces.imachine_service import IMachineService
from src.application.interfaces.icreate_community import ICreateCommunity
from src.application.interfaces.icommunity_repository import ICommunityRepository
from src.application.interfaces.imember_repository import IMemberRepository
from src.application.interfaces.iidea_repository import IIdeaRepository
from src.application.interfaces.iopinion_repository import IOpinionRepository
from src.application.interfaces.iid_generator_service import IIdGeneratorService
from src.domain.entities.community import Community
from src.domain.entities.member import Member


class CreateCommunity(ICreateCommunity):
    """Class to create a community"""

    def __init__(self,
                 community_repository: ICommunityRepository,
                 member_repository: IMemberRepository,
                 idea_repository: IIdeaRepository,
                 opinion_repository: IOpinionRepository,
                 id_generator_service: IIdGeneratorService,
                 machine_service: IMachineService):
        self.community_repository = community_repository
        self.member_repository = member_repository
        self.idea_repository = idea_repository
        self.opinion_repository = opinion_repository
        self.id_generator_service = id_generator_service
        self.machine_service = machine_service

    def execute(self, name: str, description: str):
        community = Community(
            self.id_generator_service.generate(),
            name,
            description
        )
        member = Member(
            self.machine_service.get_auth_key(None),
            self.machine_service.get_ip_address()
        )
        community.add_member(member)

        self.community_repository.add_community(
            community,
            member.authentication_key
        )
        self.member_repository.initialize_if_not_exists(community.identifier)
        self.member_repository.add_member_to_community(
            community.identifier,
            member
        )
        self.idea_repository.initialize_if_not_exists(community.identifier)
        self.opinion_repository.initialize_if_not_exists(community.identifier)
