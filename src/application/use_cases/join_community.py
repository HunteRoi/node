from src.application.interfaces.ijoin_community import IJoinCommunity
from src.application.interfaces.imachine_service import IMachineService
from src.application.exceptions.authentification_failed_error import (
    AuthentificationFailedError,
)
from src.application.interfaces.iasymetric_encryption_service import (
    IAsymetricEncryptionService,
)
from src.application.interfaces.iclient_socket import IClientSocket


class JoinCommunity(IJoinCommunity):
    """Join a community with a member"""

    def __init__(
        self,
        encryption_service: IAsymetricEncryptionService,
        machine_service: IMachineService,
    ):
        self.encryption_service = encryption_service
        self.machine_service = machine_service

        self.public_key: str
        self.private_key: str
        self.member_public_key: str

    def execute(self, client_socket: IClientSocket):
        print("Received invitation to join community")
        (
            self.public_key,
            self.private_key,
        ) = self.machine_service.get_asymetric_key_pair()

        error_message = "Failure!"
        try:
            self._send_public_key(client_socket)
            self.member_public_key = self._receive_public_key(client_socket)

            auth_key = self._receive_auth_key(client_socket)
            self._send_confirm_auth_key(client_socket, auth_key)

            symetric_key = self._receive_symetric_key(client_socket)
            return symetric_key
        except AuthentificationFailedError as error:
            return error.inner_error
        except:
            return error_message
        finally:
            client_socket.close_connection()

    def _send_public_key(self, client_socket: IClientSocket) -> str:
        """Response to the invitation"""
        print("Sending public key")
        client_socket.send_message(self.public_key)

    def _receive_public_key(self, client_socket: IClientSocket) -> str:
        """Receive the public key"""
        print("Waiting for public key")
        public_key, _ = client_socket.receive_message()

        if not public_key:
            raise AuthentificationFailedError("No public key received")
        print("Public key received")
        return public_key

    def _receive_auth_key(self, client_socket: IClientSocket) -> str:
        """Receive the auth key"""
        print("Waiting for auth key")
        encrypted_auth_key, _ = client_socket.receive_message()
        if not encrypted_auth_key:
            raise AuthentificationFailedError("Authentification key not valid")
        print("Auth key received")
        print("Decrypting auth key")
        decripted_auth_key = self.encryption_service.decrypt(
            encrypted_auth_key, self.private_key
        )
        return decripted_auth_key

    def _send_confirm_auth_key(self, client_socket: IClientSocket, auth_key: str):
        """Send the auth key to the server"""
        print("Encrypting auth key")
        reencripted_auth_key = self.encryption_service.encrypt(
            auth_key, self.member_public_key
        )
        print("Sending auth key")
        client_socket.send_message(reencripted_auth_key)

    def _receive_symetric_key(self, client_socket: IClientSocket) -> str:
        """Receive the symetric key"""
        print("Waiting for symetric key")
        encrypted_symetric_key, _ = client_socket.receive_message()

        if encrypted_symetric_key.startswith("REJECT"):
            print("Invitation rejected")
            _, rejection_message = encrypted_symetric_key.split("|", maxsplit=1)
            raise AuthentificationFailedError(rejection_message)

        if not encrypted_symetric_key:
            raise AuthentificationFailedError("No symetric key received")
        print("Symetric key received")
        print("Decrypting symetric key")
        hex_symetric_key = self.encryption_service.decrypt(
            encrypted_symetric_key, self.private_key
        )
        symetric_key = bytes.fromhex(hex_symetric_key)

        return symetric_key
