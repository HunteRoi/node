from unittest import mock
from unittest.mock import MagicMock
import pytest

from src.application.use_cases.join_community import JoinCommunity


class TestJoinCommunity:
    """Test class for the JointCommunity use case"""

    @pytest.fixture(scope="function", autouse=True, name="join_community_use_case")
    @mock.patch(
        "src.application.interfaces.icommunity_repository",
        name="community_repository",
    )
    @mock.patch(
        "src.application.interfaces.ifile_service",
        name="file_service",
    )
    @mock.patch(
        "src.application.interfaces.imachine_service",
        name="machine_service",
    )
    @mock.patch(
        "src.application.interfaces.iasymetric_encryption_service",
        name="asymetric_encryption_service",
    )
    @mock.patch(
        "src.application.interfaces.isymetric_encryption_service",
        name="symetric_encryption_service",
    )
    def create_join_community_use_case(
        self,
        symetric_encryption_service: MagicMock,
        asymetric_encryption_service: MagicMock,
        machine_service: MagicMock,
        file_service: MagicMock,
        community_repository: MagicMock,
    ) -> JoinCommunity:
        """Create the use case for join the community"""
        machine_service.get_asymetric_key_pair.return_value = (
            "public_key",
            "private_key",
        )
        symetric_encryption_service.decrypt.side_effect = [
            "id,name,description,2021-01-01T00:00:00",
            "6465637279707465645f6461746162617365",
        ]
        asymetric_encryption_service.encrypt.return_value = "encr_auth_key"
        asymetric_encryption_service.decrypt.side_effect = [
            "auth_key",
            "symetric_key",
        ]

        return JoinCommunity(
            "base_path",
            "keys_folder_path",
            symetric_encryption_service,
            asymetric_encryption_service,
            machine_service,
            file_service,
            community_repository,
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
            tuple(["INFORMATIONS|nonce,tag,encr_community_informations", member]),
            tuple(["DATABASE|nonce,tag,encrypted_database", member]),
        ]
        return mock_client

    def test_send_public_key_to_response_to_send_invitation(
        self, join_community_use_case: JoinCommunity, mock_client: MagicMock
    ):
        """Test that the public key is sent to response to send invitation"""
        join_community_use_case.execute(mock_client)

        mock_client.send_message.assert_any_call("public_key")

    def test_received_auth_key_decryption(
        self, join_community_use_case: JoinCommunity, mock_client: MagicMock
    ):
        """Test that the received auth key is decrypted"""
        join_community_use_case.execute(mock_client)

        join_community_use_case.asymetric_encryption_service.decrypt.assert_any_call(
            "encr_auth_key", "private_key"
        )

    def test_auth_key_decrypted_encryption_again(
        self, join_community_use_case: JoinCommunity, mock_client: MagicMock
    ):
        """Test that the received auth key decrypted is encrypted again"""
        join_community_use_case.execute(mock_client)

        join_community_use_case.asymetric_encryption_service.encrypt.assert_any_call(
            "auth_key", "public_key"
        )

    def test_send_encr_auth_key_to_send_confirm_auth_key(
        self, join_community_use_case: JoinCommunity, mock_client: MagicMock
    ):
        """Test that the encrypted auth key is sent to confirm auth key"""
        join_community_use_case.execute(mock_client)

        mock_client.send_message.assert_any_call("encr_auth_key")

    def test_received_symetric_key_decryption(
        self, join_community_use_case: JoinCommunity, mock_client: MagicMock
    ):
        """Test that the symetric key is decrypted"""
        join_community_use_case.execute(mock_client)

        join_community_use_case.asymetric_encryption_service.decrypt.assert_any_call(
            "encr_symetric_key", "private_key"
        )

    def test_received_community_informations_decryption(
        self, join_community_use_case: JoinCommunity, mock_client: MagicMock
    ):
        """Test that the community informations are decrypted"""
        join_community_use_case.execute(mock_client)

        join_community_use_case.symetric_encryption_service.decrypt.assert_any_call(
            "encr_community_informations", "symetric_key", "tag", "nonce"
        )

    def test_save_symetric_key(
        self, join_community_use_case: JoinCommunity, mock_client: MagicMock
    ):
        """Test that the symetric key is saved"""
        join_community_use_case.execute(mock_client)

        join_community_use_case.file_service.write_file.assert_any_call(
            "keys_folder_path/id.key", "symetric_key"
        )

    def test_save_community_informations(
        self, join_community_use_case: JoinCommunity, mock_client: MagicMock
    ):
        """Test that the community informations are saved"""
        join_community_use_case.execute(mock_client)

        join_community_use_case.community_repository.add_community.assert_called_once()

    def test_send_acknowledgement(
        self, join_community_use_case: JoinCommunity, mock_client: MagicMock
    ):
        """Test that the acknowledgement is sent"""
        join_community_use_case.execute(mock_client)

        mock_client.send_message.assert_any_call("ACK")

    def test_received_community_database_decryption(
        self, join_community_use_case: JoinCommunity, mock_client: MagicMock
    ):
        """Test that the community database is decrypted"""
        join_community_use_case.execute(mock_client)

        join_community_use_case.symetric_encryption_service.decrypt.assert_any_call(
            "encrypted_database", "symetric_key", "tag", "nonce"
        )

    def test_save_community_database(
        self, join_community_use_case: JoinCommunity, mock_client: MagicMock
    ):
        """Test that the community database is saved"""
        join_community_use_case.execute(mock_client)

        join_community_use_case.file_service.write_file.assert_any_call(
            "base_path/id.sqlite", b"decrypted_database"
        )

    def test_connection_closed(
        self,
        join_community_use_case: JoinCommunity,
        mock_client: MagicMock,
    ):
        """Test that the connection is closed"""
        join_community_use_case.execute(mock_client)

        mock_client.close_connection.assert_called_once()
