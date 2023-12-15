from unittest import mock
from unittest.mock import MagicMock
import pytest


from src.domain.entities.member import Member
from src.application.use_cases.add_member import AddMember


class TestAddMember:
    """Test add member to a community"""

    @pytest.fixture(scope="function", autouse=True, name="add_member_usecase")
    @mock.patch(
        "src.application.interfaces.imember_repository", name="member_repository"
    )
    @mock.patch(
        "src.application.interfaces.icommunity_repository", name="community_repository"
    )
    @mock.patch("src.application.interfaces.ifile_service", name="file_service")
    @mock.patch("src.application.interfaces.imachine_service", name="machine_service")
    @mock.patch(
        "src.application.interfaces.iasymetric_encryption_service",
        name="encryption_service",
    )
    @mock.patch(
        "src.application.interfaces.iid_generator_service", name="uuid_generator"
    )
    def create_add_member_usecase(
        self,
        uuid_generator: MagicMock,
        encryption_service: MagicMock,
        machine_service: MagicMock,
        file_service: MagicMock,
        community_repository: MagicMock,
        member_repository: MagicMock,
    ) -> AddMember:
        """Create a use case for adding a member to a community."""
        uuid_generator.generate.return_value = "auth_code"
        community_repository.get_community_encryption_key_path.return_value = (
            "symetric_key_path"
        )
        encryption_service.encrypt.side_effect = [
            "encr_auth_key",
            "encr_symetric_key",
        ]
        encryption_service.decrypt.return_value = "auth_code"
        machine_service.get_asymetric_key_pair.return_value = (
            "public_key",
            "private_key",
        )
        file_service.read_file.return_value = "symetric_key"
        return AddMember(
            uuid_generator,
            encryption_service,
            machine_service,
            file_service,
            community_repository,
            member_repository,
        )

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_connect_to_server_successful(
        self,
        mock_client: MagicMock,
        add_member_usecase: AddMember,
    ):
        """Test succefull connection to the guest"""
        guest = tuple(["127.0.0.1", 1111])
        mock_client.receive_message.side_effect = [
            tuple(["public_key", guest]),
            tuple(["encr_auth_code", guest]),
        ]
        mock_client.return_value = mock_client

        ip_address = "127.0.0.1"
        port = 1024

        add_member_usecase.execute("abc", ip_address, port)

        mock_client.connect_to_server.assert_called_once()

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_send_invitation(
        self,
        mock_client: MagicMock,
        add_member_usecase: AddMember,
    ):
        """Method to test send invitation to the guest with member public key"""
        guest = tuple(["127.0.0.1", 1111])
        mock_client.receive_message.side_effect = [
            tuple(["public_key", guest]),
            tuple(["encr_auth_code", guest]),
        ]
        mock_client.return_value = mock_client

        add_member_usecase.execute("abc", "127.0.0.1", 1024)

        mock_client.send_message.assert_any_call("INVITATION")

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_send_public_key(
        self,
        mock_client: MagicMock,
        add_member_usecase: AddMember,
    ):
        """Method to test send public key to the guest"""
        guest = tuple(["127.0.0.1", 1111])
        mock_client.receive_message.side_effect = [
            tuple(["public_key", guest]),
            tuple(["encr_auth_code", guest]),
        ]
        mock_client.return_value = mock_client

        add_member_usecase.execute("abc", "127.0.0.1", 1024)

        mock_client.send_message.assert_any_call("public_key")

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_auth_key_generate(
        self,
        mock_client: MagicMock,
        add_member_usecase: AddMember,
    ):
        """Method to test that an auth key is generated"""
        guest = tuple(["127.0.0.1", 1111])
        mock_client.receive_message.side_effect = [
            tuple(["public_key", guest]),
            tuple(["encr_auth_code", guest]),
        ]
        mock_client.return_value = mock_client

        add_member_usecase.execute("abc", "127.0.0.1", 1234)

        add_member_usecase.uuid_generator.generate.assert_called_once()

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_auth_key_encryption(
        self,
        mock_client: MagicMock,
        add_member_usecase: AddMember,
    ):
        """Method to test that the generated auth key is encrypted"""
        guest = tuple(["127.0.0.1", 1111])
        mock_client.receive_message.side_effect = [
            tuple(["public_key", guest]),
            tuple(["encr_auth_code", guest]),
        ]
        mock_client.return_value = mock_client

        add_member_usecase.execute("abc", "127.0.0.1", 1234)

        add_member_usecase.encryption_service.encrypt.assert_any_call(
            "auth_code", "public_key"
        )

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_auth_key_sent(
        self,
        mock_client: MagicMock,
        add_member_usecase: AddMember,
    ):
        """Method to test that the encrypted auth key is sent to the guest"""
        guest = tuple(["127.0.0.1", 1111])
        mock_client.receive_message.side_effect = [
            tuple(["public_key", guest]),
            tuple(["encr_auth_code", guest]),
        ]
        mock_client.return_value = mock_client

        add_member_usecase.execute("abc", "127.0.0.1", 1234)

        mock_client.send_message.assert_any_call("encr_auth_key")

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_auth_key_decryption(
        self,
        mock_client: MagicMock,
        add_member_usecase: AddMember,
    ):
        """Method to test that the received auth key is decrypted"""
        guest = tuple(["127.0.0.1", 1111])
        mock_client.receive_message.side_effect = [
            tuple(["public_key", guest]),
            tuple(["encr_auth_code", guest]),
        ]
        mock_client.return_value = mock_client

        add_member_usecase.execute("abc", "127.0.0.1", 1234)

        add_member_usecase.encryption_service.decrypt.assert_called_once_with(
            "encr_auth_code", "private_key"
        )

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_auth_key_not_same(
        self,
        mock_client: MagicMock,
        add_member_usecase: AddMember,
    ):
        """Method to test that the received auth key is the same as the generated one"""
        guest = tuple(["127.0.0.1", 1111])
        mock_client.receive_message.side_effect = [
            tuple(["public_key", guest]),
            tuple(["encr_auth_code", guest]),
        ]
        mock_client.return_value = mock_client

        add_member_usecase.encryption_service.decrypt.return_value = "other_auth_code"

        add_member_usecase.execute("abc", "127.0.0.1", 1234)

        mock_client.send_message.assert_any_call(
            "REJECT|Authentification key not valid"
        )

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_add_member_to_community(
        self,
        mock_client: MagicMock,
        add_member_usecase: AddMember,
    ):
        """Method to test add that the guest is added to the community"""
        guest = tuple(["127.0.0.1", 1111])
        mock_client.receive_message.side_effect = [
            tuple(["public_key", guest]),
            tuple(["encr_auth_code", guest]),
        ]
        mock_client.return_value = mock_client

        ip_address = "127.0.0.1"
        port = 1024

        member = Member("auth_code", ip_address, port)
        community_id = "abc"

        add_member_usecase.execute(community_id, ip_address, port)

        add_member_usecase.member_repository.add_member_to_community.assert_called_once_with(
            community_id, member
        )

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_get_symetric_key_path(
        self,
        mock_client: MagicMock,
        add_member_usecase: AddMember,
    ):
        """Method to test that the community symetric key is retrieved"""
        guest = tuple(["127.0.0.1", 1111])
        mock_client.receive_message.side_effect = [
            tuple(["public_key", guest]),
            tuple(["encr_auth_code", guest]),
        ]
        mock_client.return_value = mock_client

        add_member_usecase.execute("abc", "127.0.0.1", 1234)

        add_member_usecase.community_repository.get_community_encryption_key_path.assert_called_once()

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_read_symetric_key(
        self,
        mock_client: MagicMock,
        add_member_usecase: AddMember,
    ):
        """Method to test that the symetric key is read"""
        guest = tuple(["127.0.0.1", 1111])
        mock_client.receive_message.side_effect = [
            tuple(["public_key", guest]),
            tuple(["encr_auth_code", guest]),
        ]
        mock_client.return_value = mock_client

        add_member_usecase.execute("abc", "127.0.0.1", 1234)

        add_member_usecase.file_service.read_file.assert_called_once_with(
            "symetric_key_path"
        )

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_encrypt_symetric_key(
        self,
        mock_client: MagicMock,
        add_member_usecase: AddMember,
    ):
        """Method to test that the symetric key is encrypted"""
        guest = tuple(["127.0.0.1", 1111])
        mock_client.receive_message.side_effect = [
            tuple(["public_key", guest]),
            tuple(["encr_auth_code", guest]),
        ]
        mock_client.return_value = mock_client

        add_member_usecase.execute("abc", "127.0.0.1", 1234)

        add_member_usecase.encryption_service.encrypt.assert_any_call(
            "symetric_key", "public_key"
        )

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_send_symetric_key(
        self,
        mock_client: MagicMock,
        add_member_usecase: AddMember,
    ):
        """Method to test that the symetric key is sent to the guest"""
        guest = tuple(["127.0.0.1", 1111])
        mock_client.receive_message.side_effect = [
            tuple(["public_key", guest]),
            tuple(["encr_auth_code", guest]),
        ]
        mock_client.return_value = mock_client

        add_member_usecase.execute("abc", "127.0.0.1", 1234)

        mock_client.send_message.assert_any_call("encr_symetric_key")

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_reject_message_sent(
        self,
        mock_client: MagicMock,
        add_member_usecase: AddMember,
    ):
        """Method to test that the reject message is sent to the guest"""
        guest = tuple(["127.0.0.1", 1111])
        mock_client.receive_message.side_effect = [
            tuple(["public_key", guest]),
            tuple(["encr_auth_code", guest]),
        ]
        mock_client.return_value = mock_client

        add_member_usecase.encryption_service.decrypt.return_value = "other_auth_code"

        add_member_usecase.execute("abc", "127.0.0.1", 1234)

        mock_client.send_message.assert_any_call(
            "REJECT|Authentification key not valid"
        )

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_connection_closed(
        self,
        mock_client: MagicMock,
        add_member_usecase: AddMember,
    ):
        """Method to test that the connection with the guest is closed"""
        guest = tuple(["127.0.0.1", 1111])
        mock_client.receive_message.side_effect = [
            tuple(["public_key", guest]),
            tuple(["encr_auth_code", guest]),
        ]
        mock_client.return_value = mock_client

        add_member_usecase.execute("abc", "127.0.0.1", 1234)

        mock_client.close_connection.assert_called_once()

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_add_member_connection_failed(
        self,
        mock_client: MagicMock,
        add_member_usecase: AddMember,
    ):
        """Method to test that the connection with the guest is closed"""
        guest = tuple(["127.0.0.1", 1111])
        mock_client.receive_message.side_effect = [
            tuple(["public_key", guest]),
            tuple(["encr_auth_code", guest]),
        ]
        mock_client.return_value = mock_client

        mock_client.connect_to_server.side_effect = Exception()

        message = add_member_usecase.execute("abc", "127.0.0.1", 1234)

        assert message == "Failure!"
