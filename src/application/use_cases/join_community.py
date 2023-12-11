import re
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
        client_socket: IClientSocket,
    ):
        self.encryption_service = encryption_service
        self.machine_service = machine_service
        self.client_socket = client_socket

        self.public_key: str
        self.private_key: str
        self.member_public_key: str
        self.symetric_key: str

    def execute(self):
        (
            self.public_key,
            self.private_key,
        ) = self.machine_service.get_asymetric_key_pair()

        error_message = "Failure!"
        try:
            self.member_public_key = self._respond_to_send_invitation()
            self._send_confirm_auth_key()
            self.symetric_key = self._receive_symetric_key()
            return "Success!"
        except AuthentificationFailedError as error:
            return error.inner_error
        except:
            return error_message
        finally:
            self._close_connection()

    def _respond_to_send_invitation(self) -> str:
        """Response to the invitation"""
        public_key, _ = self.client_socket.receive_message()

        if not public_key:
            raise AuthentificationFailedError("No public key received")
        self.client_socket.send_message(self.public_key)

        return public_key

    def _send_confirm_auth_key(self):
        """Send the auth key to the server"""
        encrypted_auth_key, _ = self.client_socket.receive_message()
        if not encrypted_auth_key:
            raise AuthentificationFailedError("Authentification key not valid")

        decripted_auth_key = self.encryption_service.decrypt(
            encrypted_auth_key, self.private_key
        )

        reencripted_auth_key = self.encryption_service.encrypt(
            decripted_auth_key, self.member_public_key
        )

        self.client_socket.send_message(reencripted_auth_key)

    def _receive_symetric_key(self) -> str:
        """Receive the symetric key"""
        encrypted_symetric_key, _ = self.client_socket.receive_message()

        if encrypted_symetric_key.startswith("REJECT"):
            _, rejection_message = encrypted_symetric_key.split("|", 1)
            raise AuthentificationFailedError(rejection_message)

        if not encrypted_symetric_key:
            raise AuthentificationFailedError("No symetric key received")

        symetric_key = self.encryption_service.decrypt(
            encrypted_symetric_key, self.private_key
        )

        return symetric_key

    def _close_connection(self):
        self.client_socket.close_connection()
