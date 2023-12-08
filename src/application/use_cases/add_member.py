from src.domain.entities.member import Member
from src.application.exceptions.authentification_failed_error import (
    AuthentificationFailedError,
)
from src.application.interfaces.iasymetric_encryption_service import (
    IAsymetricEncryptionService,
)
from src.application.interfaces.iid_generator_service import IIdGeneratorService
from src.application.interfaces.imachine_service import IMachineService
from src.application.interfaces.ifile_service import IFileService
from src.application.interfaces.icommunity_repository import ICommunityRepository
from src.application.interfaces.imember_repository import IMemberRepository
from src.application.interfaces.iadd_member import IAddMember
from src.application.interfaces.iclient_socket import IClientSocket


class AddMember(IAddMember):
    """Add a member to a community"""

    def __init__(
        self,
        uuid_generator: IIdGeneratorService,
        encryption_service: IAsymetricEncryptionService,
        machine_service: IMachineService,
        file_service: IFileService,
        client_socket: IClientSocket,
        community_repository: ICommunityRepository,
        member_repository: IMemberRepository,
    ):
        self.encryption_service = encryption_service
        self.uuid_generator = uuid_generator
        self.machine_service = machine_service
        self.file_service = file_service
        self.client_socket = client_socket
        self.community_repository = community_repository
        self.member_repository = member_repository

        self.public_key: str
        self.private_key: str
        self.guest_public_key: str

    def execute(self, community_id: str, ip_address: str, port: int):
        (
            self.public_key,
            self.private_key,
        ) = self.machine_service.get_asymetric_key_pair()

        self._connect_to_guest(ip_address, port)

        self.guest_public_key = self._send_invitation()

        try:
            auth_key = self._send_auth_key()

            self._add_member_to_community(community_id, auth_key, ip_address, port)

            self._send_community_symetric_key(community_id)
        except AuthentificationFailedError as error:
            self._send_reject_message(error.inner_error)
            raise error
        finally:
            self._close_connection()

    def _connect_to_guest(self, ip_address: str, port: int):
        self.client_socket.connect_to_server(ip_address, port)

    def _send_invitation(self) -> str:
        self.client_socket.send_message(f"INVITATION|{self.public_key}")

        public_key, _ = self.client_socket.receive_message()

        if not public_key:
            raise AuthentificationFailedError("No public key received")
        return public_key

    def _send_auth_key(self) -> str:
        """Give the auth key to the new member"""
        auth_key = self.uuid_generator.generate()

        encrypted_auth_key = self.encryption_service.encrypt(
            auth_key, self.guest_public_key
        )

        self.client_socket.send_message(encrypted_auth_key)

        reencrypted_auth_key, _ = self.client_socket.receive_message()

        decrypted_auth_key = self.encryption_service.decrypt(
            reencrypted_auth_key, self.private_key
        )

        if decrypted_auth_key != auth_key:
            raise AuthentificationFailedError("Authentification key not valid")
        return auth_key

    def _add_member_to_community(
        self, community_id: str, auth_key: str, ip_address: str, port: int
    ):
        member = Member(auth_key, ip_address, port)
        self.member_repository.add_member_to_community(community_id, member)

    def _send_community_symetric_key(self, community_id: str):
        """Send the symetric key to the new member"""
        symetric_key_path = self.community_repository.get_community_encryption_key_path(
            community_id
        )
        symetric_key = self.file_service.read_file(symetric_key_path, with_binary_format=True)

        encrypted_symetric_key = self.encryption_service.encrypt(
            symetric_key, self.guest_public_key
        )

        self.client_socket.send_message(encrypted_symetric_key)

    def _send_reject_message(self, message: str):
        self.client_socket.send_message(f"REJECT|{message}")

    def _close_connection(self):
        self.client_socket.close_connection()
