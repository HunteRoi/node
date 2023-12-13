from src.application.interfaces.imachine_service import IMachineService
from src.application.interfaces.icreate_community import ICreateCommunity
from src.application.interfaces.icommunity_repository import ICommunityRepository
from src.application.interfaces.imember_repository import IMemberRepository
from src.application.interfaces.iidea_repository import IIdeaRepository
from src.application.interfaces.iopinion_repository import IOpinionRepository
from src.application.interfaces.iid_generator_service import IIdGeneratorService
from src.application.interfaces.isymetric_encryption_service import (
    ISymetricEncryptionService,
)
from src.application.interfaces.ifile_service import IFileService
from src.domain.entities.community import Community
from src.domain.entities.member import Member


class CreateCommunity(ICreateCommunity):
    """Class to create a community"""

    def __init__(
        self,
        keys_folder_path: str,
        community_repository: ICommunityRepository,
        member_repository: IMemberRepository,
        idea_repository: IIdeaRepository,
        opinion_repository: IOpinionRepository,
        id_generator_service: IIdGeneratorService,
        encryption_service: ISymetricEncryptionService,
        machine_service: IMachineService,
        file_service: IFileService,
    ):
        self.keys_folder_path = keys_folder_path
        self.community_repository = community_repository
        self.member_repository = member_repository
        self.idea_repository = idea_repository
        self.opinion_repository = opinion_repository
        self.id_generator_service = id_generator_service
        self.encryption_service = encryption_service
        self.machine_service = machine_service
        self.file_service = file_service

    def execute(self, name: str, description: str):
        member = self._create_member()
        community = self._create_community(name, description, member)

        encryption_key_path = self._generate_community_key(community.identifier)

        self.community_repository.add_community(
            community, member.authentication_key, encryption_key_path
        )

        self._initialize_community_database(community.identifier, member)

    def _create_member(self) -> Member:
        return self.machine_service.get_current_user()

    def _create_community(
        self, name: str, description: str, member: Member
    ) -> Community:
        community = Community(self.id_generator_service.generate(), name, description)
        community.add_member(member)
        return community

    def _generate_community_key(self, community_id: str) -> str:
        key = self.encryption_service.generate_key()
        encryption_key_path = f"{self.keys_folder_path}/{community_id}.key"
        self.file_service.write_file(encryption_key_path, key)
        return encryption_key_path

    def _initialize_community_database(self, community_id: str, member: Member) -> None:
        self.member_repository.initialize_if_not_exists(community_id)
        self.member_repository.add_member_to_community(community_id, member)
        self.idea_repository.initialize_if_not_exists(community_id)
        self.opinion_repository.initialize_if_not_exists(community_id)
