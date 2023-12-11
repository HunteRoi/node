from unittest import mock
from unittest.mock import MagicMock
import pytest

from src.application.use_cases.join_community import JoinCommunity


class TestJoinCommunity:
    """Test class for the JointCommunity use case"""

    @pytest.fixture(scope="function", autouse=True, name="join_community_use_case")
    @mock.patch(
        "src.application.interfaces.iasymetric_encryption_service.IAsymetricEncryptionService",
        name="encryption_service",
    )
    @mock.patch(
        "src.application.interfaces.imachine_service.IMachineService",
        name="machine_service",
    )
    @mock.patch(
        "src.application.interfaces.iclient_socket.IClientSocket", name="mock_client"
    )
    def create_join_community_use_case(
        self,
        encryption_service: MagicMock,
        machine_service: MagicMock,
        mock_client: MagicMock,
    ) -> JoinCommunity:
        """Create the use case for join the community"""
        member = tuple(["127.0.0.1", 1111])
        mock_client.receive_message.side_effect = [
            tuple(["public_key", member]),
            tuple(["auth_key", member]),
            tuple(["symetric_key", member]),
        ]
        machine_service.get_asymetric_key_pair.return_value = (
            "public_key",
            "private_key",
        )

        encryption_service.encrypt.return_value = "encrypted_value"
        encryption_service.decrypt.return_value = "decrypted_value"

        return JoinCommunity(
            encryption_service,
            machine_service,
            mock_client,
        )

    def test_send_public_key_to_response_to_send_invitation(
        self, join_community_use_case: JoinCommunity
    ):
        """method to send public key to response to send invitation"""
        join_community_use_case.execute()
        join_community_use_case.client_socket.send_message.assert_any_call("public_key")

    def test_auth_key_decription(self, join_community_use_case: JoinCommunity):
        """method to test the auth key decription"""
        join_community_use_case.execute()
        join_community_use_case.encryption_service.decrypt.assert_any_call(
            "auth_key", "private_key"
        )

    def test_auth_key_encryption_to_send_confirm_auth_key(
        self, join_community_use_case: JoinCommunity
    ):
        """method to test the auth key encryption to send confirm auth key"""
        join_community_use_case.execute()
        join_community_use_case.encryption_service.encrypt.assert_any_call(
            mock.ANY, "public_key"
        )

    def test_send_encr_auth_key_to_send_confirm_auth_key(
        self, join_community_use_case: JoinCommunity
    ):
        """method to send encr auth key to send confirm auth key"""
        join_community_use_case.execute()
        join_community_use_case.client_socket.send_message.assert_any_call(mock.ANY)

    def test_receive_symetric_key(self, join_community_use_case: JoinCommunity):
        """method to receive symetric key"""
        join_community_use_case.execute()
        join_community_use_case.client_socket.receive_message.assert_any_call()
        join_community_use_case.encryption_service.decrypt.assert_called_with(
            mock.ANY, "private_key"
        )

    def test_connection_closed(
        self,
        join_community_use_case: JoinCommunity,
    ):
        """Method to test that the connection with the guest is closed"""
        join_community_use_case.execute()

        join_community_use_case.client_socket.close_connection.assert_called_once()
