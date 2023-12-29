import socket

from src.application.interfaces.idatetime_service import IDatetimeService
from src.application.interfaces.imachine_service import IMachineService
from src.application.interfaces.icommunity_repository import ICommunityRepository
from src.application.interfaces.iid_generator_service import IIdGeneratorService
from src.application.interfaces.iasymetric_encryption_service import (
    IAsymetricEncryptionService,
)
from src.application.interfaces.ifile_service import IFileService
from src.domain.entities.member import Member


class MachineService(IMachineService):
    """Class to get machine information"""

    def __init__(
        self,
        base_path: str,
        community_repository: ICommunityRepository,
        id_generator_service: IIdGeneratorService,
        encryption_service: IAsymetricEncryptionService,
        file_service: IFileService,
        datetime_service: IDatetimeService,
    ):
        self.base_path = base_path
        self.community_repository = community_repository
        self.id_generator_service = id_generator_service
        self.encryption_service = encryption_service
        self.file_service = file_service
        self.datetime_service = datetime_service

    def get_ip_address(self) -> str:
        dns_socket: socket.socket | None = None
        try:
            dns_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            dns_socket.connect(("8.8.8.8", 80))
            return dns_socket.getsockname()[0]
        except:
            return socket.gethostbyname(socket.gethostname())
        finally:
            if dns_socket is not None:
                dns_socket.close()

    def get_auth_key(self, community_id: str | None = None) -> str:
        if community_id is None:
            return self.id_generator_service.generate()
        return self.community_repository.get_authentication_key_for_community(
            community_id
        )

    def get_asymetric_key_pair(self) -> tuple[str, str]:
        public_key_file = f"{self.base_path}/encryption_key.pub"
        private_key_file = f"{self.base_path}/encryption_key"

        try:
            public_key = self.file_service.read_file(public_key_file)
            private_key = self.file_service.read_file(private_key_file)
        except FileNotFoundError:
            public_key, private_key = self.encryption_service.generate_keys()
            self.file_service.write_file(public_key_file, public_key)
            self.file_service.write_file(private_key_file, private_key)
        return public_key, private_key

    def get_port(self) -> int:
        return 1664

    def get_current_user(self, community_id: str | None = None) -> Member:
        return Member(
            self.get_auth_key(community_id),
            self.get_ip_address(),
            self.get_port(),
            self.datetime_service.get_datetime(),
        )
