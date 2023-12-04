import os

from src.application.interfaces.imachine_service import IMachineService
from src.application.interfaces.iid_generator_service import IIdGeneratorService
from src.application.interfaces.iasymetric_encryption_service import (
    IAsymetricEncryptionService,
)
from src.application.interfaces.isymetric_encryption_service import (
    ISymetricEncryptionService,
)
from src.application.interfaces.iclient_socket import IClientSocket
from src.application.interfaces.ifile_service import IFileService
from src.application.interfaces.icommunity_repository import ICommunityRepository
from src.application.interfaces.imember_repository import IMemberRepository
from src.application.interfaces.iidea_repository import IIdeaRepository
from src.application.interfaces.iopinion_repository import IOpinionRepository
from src.infrastructure.repositories.community_repository import CommunityRepository
from src.infrastructure.repositories.member_repository import MemberRepository
from src.infrastructure.repositories.idea_repository import IdeaRepository
from src.infrastructure.repositories.opinion_repository import OpinionRepository
from src.infrastructure.services.uuid_generator_service import UuidGeneratorService
from src.infrastructure.services.machine_service import MachineService
from src.infrastructure.services.asymetric_encryption_service import (
    AsymetricEncryptionService,
)
from src.infrastructure.services.symetric_encryption_service import (
    SymetricEncryptionService,
)
from src.presentation.network.client import Client
from src.infrastructure.services.file_service import FileService
from src.application.use_cases.create_community import CreateCommunity
from src.application.use_cases.add_member import AddMember
from src.application.use_cases.read_communities import ReadCommunities
from src.application.use_cases.read_ideas_from_community import ReadIdeasFromCommunity
from src.application.use_cases.read_opinions import ReadOpinions
from src.presentation.views.menus.main_menu import MainMenu


class Application:
    """The application's entry point."""

    machine_service: IMachineService
    id_generator: IIdGeneratorService
    asymetric_encryption_service: IAsymetricEncryptionService
    symetric_encryption_service: ISymetricEncryptionService
    client_socket: IClientSocket
    file_service: IFileService
    community_repository: ICommunityRepository
    member_repository: IMemberRepository
    idea_repository: IIdeaRepository
    opinion_repository: IOpinionRepository
    create_community_usecase: CreateCommunity
    add_member_usecase: AddMember
    read_communities_usecase: ReadCommunities
    read_ideas_from_community_usecase: ReadIdeasFromCommunity
    read_opinions_usecase: ReadOpinions

    @staticmethod
    def run():
        """Configures the dependencies and runs the application."""
        Application._prepare()

        Application.machine_service.get_asymetric_key_pair()

        MainMenu(
            Application.create_community_usecase,
            Application.add_member_usecase,
            Application.read_communities_usecase,
            Application.read_ideas_from_community_usecase,
            Application.read_opinions_usecase,
        ).show()

    @staticmethod
    def _prepare():
        # Create the data directory
        base_path = os.path.join(os.getcwd(), "data")
        os.makedirs(base_path, exist_ok=True)
        keys_path = os.path.join(base_path, "keys")
        os.makedirs(keys_path, exist_ok=True)

        # Repositories
        Application.community_repository = CommunityRepository(base_path)
        Application.member_repository = MemberRepository(base_path)
        Application.idea_repository = IdeaRepository(base_path)
        Application.opinion_repository = OpinionRepository(base_path)

        # Services
        Application.id_generator = UuidGeneratorService()
        Application.file_service = FileService()
        Application.asymetric_encryption_service = AsymetricEncryptionService()
        Application.symetric_encryption_service = SymetricEncryptionService()
        Application.machine_service = MachineService(
            base_path,
            Application.community_repository,
            Application.id_generator,
            Application.asymetric_encryption_service,
            Application.file_service,
        )

        # Network
        Application.client_socket = Client()

        # Use cases
        Application.create_community_usecase = CreateCommunity(
            keys_path,
            Application.community_repository,
            Application.member_repository,
            Application.idea_repository,
            Application.opinion_repository,
            Application.id_generator,
            Application.symetric_encryption_service,
            Application.machine_service,
            Application.file_service,
        )
        Application.add_member_usecase = AddMember(
            Application.id_generator,
            Application.asymetric_encryption_service,
            Application.client_socket,
            Application.member_repository,
        )
        Application.add_member_usecase = AddMember(
            Application.id_generator,
            Application.asymetric_encryption_service,
            Application.client_socket,
            Application.member_repository,
        )
        Application.read_communities_usecase = ReadCommunities(
            Application.community_repository
        )
        Application.read_ideas_from_community_usecase = ReadIdeasFromCommunity(
            Application.idea_repository
        )
        Application.read_opinions_usecase = ReadOpinions(Application.opinion_repository)
