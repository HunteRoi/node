import json

from src.application.interfaces.icreate_idea import ICreateIdea
from src.application.interfaces.iid_generator_service import IIdGeneratorService
from src.application.interfaces.iidea_repository import IIdeaRepository
from src.application.interfaces.imachine_service import IMachineService
from src.application.interfaces.imember_repository import IMemberRepository
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
    ):
        self.machine_service = machine_service
        self.id_generator_service = id_generator_service
        self.idea_repository = idea_repository
        self.member_repository = member_repository

    def execute(self, community_id: str, content: str):
        """Create an idea."""
        author = self.machine_service.get_current_user(community_id)
        members = filter(
            lambda member: member.authentication_key != author.authentication_key,
            self.member_repository.get_members_from_community(community_id),
        )

        idea = Idea(self.id_generator_service.generate(), content, author)
        self.idea_repository.add_idea_to_community(community_id, idea)

        for member in members:
            try:
                client_socket = client.Client()
                client_socket.connect_to_server(member.ip_address, member.port)
                print(f"Connection opened to {member.ip_address}:{member.port}")
                client_socket.send_message(f"CREATE_IDEA|{idea.to_str()}")
                print(f"Idea sent {idea.to_str()}")
            except:
                pass
            finally:
                client_socket.close_connection()
                print(f"Connection closed to {member.ip_address}:{member.port}")
