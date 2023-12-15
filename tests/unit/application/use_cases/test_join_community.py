from unittest import mock
from unittest.mock import MagicMock
import pytest

from src.application.use_cases.join_community import JoinCommunity


class TestJoinCommunity:
    """Test class for the JointCommunity use case"""

    @pytest.fixture(scope="function", autouse=True, name="join_community_use_case")
    @mock.patch(
        "src.application.interfaces.imachine_service",
        name="machine_service",
    )
    @mock.patch(
        "src.application.interfaces.iasymetric_encryption_service",
        name="encryption_service",
    )
    def create_join_community_use_case(
        self,
        encryption_service: MagicMock,
        machine_service: MagicMock,
    ) -> JoinCommunity:
        """Create the use case for join the community"""
        machine_service.get_asymetric_key_pair.return_value = (
            "public_key",
            "private_key",
        )

        encryption_service.encrypt.return_value = "encr_auth_key"
        encryption_service.decrypt.side_effect = [
            "auth_key",
            "symetric_key",
        ]

        return JoinCommunity(
            encryption_service,
            machine_service,
        )

    @pytest.fixture(scope="function", autouse=True, name="mock_client")
    @mock.patch("src.application.interfaces.iclient_socket", name="mock_client")
    def create_mock_client(self, mock_client: MagicMock) -> MagicMock:
        """Create the mock client"""
        member = tuple(["127.0.0.1", 1111])
        mock_client.receive_message.side_effect = [
            tuple(["public_key", member]),
            tuple(["encr_auth_key", member]),
            tuple(["encr_symetric_key", member]),
        ]
        return mock_client

    def test_send_public_key_to_response_to_send_invitation(
        self, join_community_use_case: JoinCommunity, mock_client: MagicMock
    ):
        """method to send public key to response to send invitation"""
        join_community_use_case.execute(mock_client)

        mock_client.send_message.assert_any_call("public_key")

    def test_auth_key_decription(
        self, join_community_use_case: JoinCommunity, mock_client: MagicMock
    ):
        """method to test the auth key decription"""
        join_community_use_case.execute(mock_client)

        join_community_use_case.encryption_service.decrypt.assert_any_call(
            "encr_auth_key", "private_key"
        )

    def test_auth_key_encryption_to_send_confirm_auth_key(
        self, join_community_use_case: JoinCommunity, mock_client: MagicMock
    ):
        """method to test the auth key encryption to send confirm auth key"""
        join_community_use_case.execute(mock_client)

        join_community_use_case.encryption_service.encrypt.assert_any_call(
            "auth_key", "public_key"
        )

    def test_send_encr_auth_key_to_send_confirm_auth_key(
        self, join_community_use_case: JoinCommunity, mock_client: MagicMock
    ):
        """method to send encr auth key to send confirm auth key"""
        join_community_use_case.execute(mock_client)

        mock_client.send_message.assert_any_call("encr_auth_key")

    def test_receive_symetric_key(
        self, join_community_use_case: JoinCommunity, mock_client: MagicMock
    ):
        """method to receive symetric key"""
        join_community_use_case.execute(mock_client)

        mock_client.receive_message.assert_any_call()
        join_community_use_case.encryption_service.decrypt.assert_called_with(
            "encr_symetric_key", "private_key"
        )

    def test_connection_closed(
        self,
        join_community_use_case: JoinCommunity,
        mock_client: MagicMock,
    ):
        """Method to test that the connection with the guest is closed"""
        join_community_use_case.execute(mock_client)

        mock_client.close_connection.assert_called_once()
