from time import sleep

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
import src.presentation.network.client as client


class AddMember(IAddMember):
    """Add a member to a community"""

    def __init__(
        self,
        uuid_generator: IIdGeneratorService,
        encryption_service: IAsymetricEncryptionService,
        machine_service: IMachineService,
        file_service: IFileService,
        community_repository: ICommunityRepository,
        member_repository: IMemberRepository,
    ):
        self.encryption_service = encryption_service
        self.uuid_generator = uuid_generator
        self.machine_service = machine_service
        self.file_service = file_service
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

        error_message = "Failure!"
        try:
            client_socket = client.Client()
            self._connect_to_guest(client_socket, ip_address, port)

            self.guest_public_key = self._receive_public_key(client_socket)
            self._send_encryption_public_key(client_socket)

            auth_key = self.uuid_generator.generate()
            self._send_auth_key(client_socket, auth_key)
            received_auth_key = self._receive_auth_key(client_socket)
            if received_auth_key != auth_key:
                raise AuthentificationFailedError("Authentification key not valid")

            self._add_member_to_community(community_id, auth_key, ip_address, port)

            self._send_community_symetric_key(client_socket, community_id)

            return "Success!"
        except AuthentificationFailedError as error:
            self._send_reject_message(client_socket, error.inner_error)
            return error_message
        except:
            return error_message
        finally:
            client_socket.close_connection()
            sleep(10)

    def _connect_to_guest(
        self, client_socket: IClientSocket, ip_address: str, port: int
    ):
        """Connect to the guest"""
        print(f"Connecting to {ip_address}:{port}")
        client_socket.connect_to_server(ip_address, port)
        print("Connected to the guest")
        print("Sending invitation")
        client_socket.send_message("INVITATION")

    def _receive_public_key(self, client_socket: IClientSocket) -> str:
        """Receive the public key from the guest"""
        print("Waiting for public key")
        public_key, _ = client_socket.receive_message()
        if not public_key:
            raise AuthentificationFailedError("No public key received")
        print("Public key received")
        return public_key

    def _send_encryption_public_key(self, client_socket: IClientSocket):
        """Send the public key to the new member"""
        print("Sending public key")
        client_socket.send_message(self.public_key)

    def _send_auth_key(self, client_socket: IClientSocket, auth_key: str):
        """Give the auth key to the new member"""
        print("Encrypt auth key")
        encrypted_auth_key = self.encryption_service.encrypt(
            auth_key, self.guest_public_key
        )
        print("Sending auth key")
        client_socket.send_message(encrypted_auth_key)

    def _receive_auth_key(self, client_socket: IClientSocket) -> str:
        """Receive the auth key"""
        print("Waiting for auth key")
        reencrypted_auth_key, _ = client_socket.receive_message()
        if not reencrypted_auth_key:
            raise AuthentificationFailedError("Authentification key not valid")
        print("Auth key received")
        print("Decrypt auth key")
        decrypted_auth_key = self.encryption_service.decrypt(
            reencrypted_auth_key, self.private_key
        )

        return decrypted_auth_key

    def _add_member_to_community(
        self, community_id: str, auth_key: str, ip_address: str, port: int
    ):
        """Add the member to the community"""
        member = Member(auth_key, ip_address, port)
        print("Adding member to community")
        self.member_repository.add_member_to_community(community_id, member)

    def _send_community_symetric_key(
        self, client_socket: IClientSocket, community_id: str
    ):
        """Send the symetric key to the new member"""
        symetric_key_path = self.community_repository.get_community_encryption_key_path(
            community_id
        )
        symetric_key = self.file_service.read_file(symetric_key_path)
        print("Encrypt symetric key")
        encrypted_symetric_key = self.encryption_service.encrypt(
            symetric_key, self.guest_public_key
        )

        print("Sending symetric key")
        client_socket.send_message(encrypted_symetric_key)

    def _send_reject_message(self, client_socket: IClientSocket, message: str):
        """Send a reject message to the new member"""
        print("Sending reject message")
        client_socket.send_message(f"REJECT|{message}")
