from src.application.interfaces.icommunity_repository import ICommunityRepository
from src.application.interfaces.icreate_idea import ICreateIdea
from src.application.interfaces.ifile_service import IFileService
from src.application.interfaces.iid_generator_service import IIdGeneratorService
from src.application.interfaces.iidea_repository import IIdeaRepository
from src.application.interfaces.imachine_service import IMachineService
from src.application.interfaces.imember_repository import IMemberRepository
from src.application.interfaces.isymetric_encryption_service import (
    ISymetricEncryptionService,
)
from src.domain.entities.idea import Idea
import src.presentation.network.client as client


class CreateIdea(ICreateIdea):
    """Create an idea."""

    def __init__(
        self,
        machine_service: IMachineService,
        id_generator_service: IIdGeneratorService,
        idea_repository: IIdeaRepository,
        member_repository: IMemberRepository,
        community_repository: ICommunityRepository,
        file_service: IFileService,
        symetric_encryption_service: ISymetricEncryptionService,
    ):
        self.machine_service = machine_service
        self.id_generator_service = id_generator_service
        self.idea_repository = idea_repository
        self.member_repository = member_repository
        self.community_repository = community_repository
        self.file_service = file_service
        self.symetric_encryption_service = symetric_encryption_service

    def _get_symetric_key(self, community_id: str):
        """Get the symetric key from the community."""
        symetric_key_path = self.community_repository.get_community_encryption_key_path(
            community_id
        )
        return self.file_service.read_file(symetric_key_path)

    def execute(self, community_id: str, content: str) -> str:
        """Create an idea."""
        try:
            symetric_key = self._get_symetric_key(community_id)
            author = self.machine_service.get_current_user(community_id)
            members = filter(
                lambda member: member.authentication_key != author.authentication_key,
                self.member_repository.get_members_from_community(community_id),
            )

            idea = Idea(self.id_generator_service.generate(), content, author)
            self.idea_repository.add_idea_to_community(community_id, idea)

            for member in members:
                client_socket: client.Client = None
                try:
                    client_socket = client.Client()
                    (nonce, tag, cipher) = self.symetric_encryption_service.encrypt(
                        idea.to_str(), symetric_key
                    )
                    client_socket.connect_to_server(member.ip_address, member.port)
                    client_socket.send_message(f"CREATE_IDEA|{nonce},{tag},{cipher}")
                except:
                    pass
                finally:
                    if client_socket is not None:
                        client_socket.close_connection()
            return "Success!"
        except Exception as error:
            return str(error)
