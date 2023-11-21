from src.domain.entities.member import Member
from src.application.exceptions.authentification_failed_error import AuthentificationFailedError
from src.application.interfaces.iencryption_asymetric_service import IEncryptionAsymetricService
from src.application.interfaces.iid_generator_service import IIdGeneratorService
from src.application.interfaces.imember_repository import IMemberRepository
from src.application.interfaces.iadd_member import IAddMember
from src.application.interfaces.iclient_socket import IClientSocket


class AddMember(IAddMember):
    """Add a member to a community"""

    def __init__(self,
                 uuid_generator: IIdGeneratorService,
                 encryption_service: IEncryptionAsymetricService,
                 client_socket: IClientSocket,
                 member_repository: IMemberRepository):
        self.encryption_service = encryption_service
        self.uuid_generator = uuid_generator
        self.client_socket = client_socket
        self.member_repository = member_repository

    def execute(self, community_id: str, ip_address: str, port: int):
        public_key = self._send_invitation(ip_address, port)

        auth_key = self._send_auth_key(public_key)

        self._add_member_to_community(community_id, auth_key, ip_address)

        self._close_connection()

    def _send_invitation(self, ip_address: str, port: int) -> str:
        self.client_socket.connect_to_server(ip_address, port)

        self.client_socket.send_message("invitation")

        public_key, _ = self.client_socket.receive_message()

        if not public_key:
            raise AuthentificationFailedError("No public key received")
        return public_key

    def _send_auth_key(self, public_key: str) -> str:
        """Give the auth key to the new member"""
        auth_key = self.uuid_generator.generate()

        encrypted_auth_key = self.encryption_service.asymetric_key_encryption(auth_key,
                                                                              public_key)

        self.client_socket.send_message(encrypted_auth_key)

        decrypted_auth_key, _ = self.client_socket.receive_message()

        if decrypted_auth_key != auth_key:
            raise AuthentificationFailedError("Authentification key not valid")
        return auth_key

    def _add_member_to_community(self, community_id: str, auth_key: str, ip_address: str):
        member = Member(auth_key, ip_address)
        self.member_repository.add_member_to_community(community_id, member)

    def _close_connection(self):
        self.client_socket.send_message(
            "You are now a member of the community")
        self.client_socket.close_connection()
