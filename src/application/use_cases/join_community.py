from src.application.interfaces.ijoin_community import IJoinCommunity
from src.application.interfaces.imachine_service import IMachineService
from src.application.interfaces.ifile_service import IFileService
from src.application.exceptions.authentification_failed_error import (
    AuthentificationFailedError,
)
from src.application.interfaces.iasymetric_encryption_service import (
    IAsymetricEncryptionService,
)
from src.application.interfaces.isymetric_encryption_service import (
    ISymetricEncryptionService,
)
from src.application.interfaces.iclient_socket import IClientSocket
from src.application.interfaces.icommunity_repository import ICommunityRepository
from src.domain.entities.community import Community


class JoinCommunity(IJoinCommunity):
    """Join a community with a member"""

    def __init__(
        self,
        base_path: str,
        keys_folder_path: str,
        symetric_encryption_service: ISymetricEncryptionService,
        asymetric_encryption_service: IAsymetricEncryptionService,
        machine_service: IMachineService,
        file_service: IFileService,
        community_repository: ICommunityRepository,
    ):
        self.base_path = base_path
        self.keys_folder_path = keys_folder_path
        self.symetric_encryption_service = symetric_encryption_service
        self.asymetric_encryption_service = asymetric_encryption_service
        self.machine_service = machine_service
        self.file_service = file_service
        self.community_repository = community_repository

        self.public_key: str
        self.private_key: str
        self.member_public_key: str
        self.symetric_key: str

    def execute(self, client_socket: IClientSocket) -> str:
        (
            self.public_key,
            self.private_key,
        ) = self.machine_service.get_asymetric_key_pair()

        try:
            self._send_public_key(client_socket)
            self.member_public_key = self._receive_public_key(client_socket)

            auth_key = self._receive_auth_key(client_socket)
            self._send_confirm_auth_key(client_socket, auth_key)

            self.symetric_key = self._receive_symetric_key(client_socket)

            community = self._receive_community_informations(client_socket)

            symetric_key_path = self._save_symetric_key(community.identifier)
            self._save_community_informations(community, auth_key, symetric_key_path)
            self._send_acknowledgement(client_socket)

            community_database = self._receive_community_database(client_socket)
            self._save_community_database(community.identifier, community_database)

            return "Success!"
        except Exception as error:
            return str(error)
        finally:
            client_socket.close_connection()

    def _send_public_key(self, client_socket: IClientSocket) -> str:
        """Response to the invitation"""
        client_socket.send_message(self.public_key)

    def _receive_public_key(self, client_socket: IClientSocket) -> str:
        """Receive the public key"""
        public_key, _ = client_socket.receive_message()

        if not public_key:
            raise AuthentificationFailedError("No public key received")

        return public_key

    def _receive_auth_key(self, client_socket: IClientSocket) -> str:
        """Receive the auth key"""
        encrypted_auth_key, _ = client_socket.receive_message()
        if not encrypted_auth_key:
            raise AuthentificationFailedError("Authentification key not valid")

        decripted_auth_key = self.asymetric_encryption_service.decrypt(
            encrypted_auth_key, self.private_key
        )
        return decripted_auth_key

    def _send_confirm_auth_key(self, client_socket: IClientSocket, auth_key: str):
        """Send the auth key to the server"""
        reencripted_auth_key = self.asymetric_encryption_service.encrypt(
            auth_key, self.member_public_key
        )

        client_socket.send_message(reencripted_auth_key)

    def _receive_symetric_key(self, client_socket: IClientSocket) -> str:
        """Receive the symetric key"""
        encrypted_symetric_key, _ = client_socket.receive_message()

        if encrypted_symetric_key.startswith("REJECT"):
            _, rejection_message = encrypted_symetric_key.split("|", maxsplit=1)
            raise AuthentificationFailedError(rejection_message)

        if not encrypted_symetric_key:
            raise AuthentificationFailedError("No symetric key received")
        symetric_key = self.asymetric_encryption_service.decrypt(
            encrypted_symetric_key, self.private_key
        )

        return symetric_key

    def _receive_community_informations(
        self, client_socket: IClientSocket
    ) -> Community:
        """Receive the community informations"""
        message, _ = client_socket.receive_message()

        if not message:
            raise AuthentificationFailedError("No community informations received")

        message = message.split("|", maxsplit=1)[1]
        nonce, tag, encr_community_informations = message.split(",", maxsplit=2)

        community_informations = self.symetric_encryption_service.decrypt(
            encr_community_informations, self.symetric_key, tag, nonce
        )

        return Community.from_str(community_informations)

    def _save_symetric_key(self, community_id: str) -> str:
        """Save the symetric key"""
        symetric_key_path = f"{self.keys_folder_path}/{community_id}.key"
        self.file_service.write_file(symetric_key_path, self.symetric_key)

        return symetric_key_path

    def _save_community_informations(
        self, community: Community, auth_key: str, symetric_key_path: str
    ):
        """Save the community informations"""
        self.community_repository.add_community(
            community,
            auth_key,
            symetric_key_path,
        )

    def _send_acknowledgement(self, client_socket: IClientSocket):
        """Send acknowledgement"""
        client_socket.send_message("ACK")

    def _receive_community_database(self, client_socket: IClientSocket):
        """Receive the community database"""
        message, _ = client_socket.receive_message()

        if not message:
            raise AuthentificationFailedError("No community database received")

        message = message.split("|", maxsplit=1)[1]
        nonce, tag, encrypted_database = message.split(",", maxsplit=2)

        decrypted_database = self.symetric_encryption_service.decrypt(
            encrypted_database, self.symetric_key, tag, nonce
        )

        return decrypted_database

    def _save_community_database(self, community_id: str, community_database: str):
        """Save the community database"""
        community_database_path = f"{self.base_path}/{community_id}.sqlite"
        database_bytes = bytes.fromhex(community_database)
        self.file_service.write_file(community_database_path, database_bytes)
