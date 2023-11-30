import socket

from src.application.interfaces.imachine_service import IMachineService
from src.application.interfaces.icommunity_repository import ICommunityRepository
from src.application.interfaces.iid_generator_service import IIdGeneratorService


class MachineService(IMachineService):
    """Class to get machine information"""

    def __init__(
        self,
        repository: ICommunityRepository,
        id_generator_service: IIdGeneratorService,
    ):
        self.repository = repository
        self.id_generator_service = id_generator_service

    def get_ip_address(self) -> str:
        return socket.gethostbyname(socket.gethostname())

    def get_auth_key(self, community_id: int | None) -> str:
        if community_id is None:
            return self.id_generator_service.generate()
        return self.repository.get_authentication_key_for_community(community_id)

    def get_port(self) -> int:
        return 0
