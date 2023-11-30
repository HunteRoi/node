from unittest import mock
from unittest.mock import MagicMock
import pytest


from src.domain.entities.member import Member
from src.application.exceptions.authentification_failed_error import (
    AuthentificationFailedError,
)
from src.application.use_cases.add_member import AddMember


class TestAddMember:
    """Test add member to a community"""

    @mock.patch(
        "src.application.interfaces.iasymetric_encryption_service",
        name="encryption_service",
    )
    @mock.patch(
        "src.application.interfaces.iid_generator_service", name="uuid_generator"
    )
    @mock.patch("src.application.interfaces.iclient_socket", name="mock_client")
    @mock.patch(
        "src.application.interfaces.imember_repository", name="member_repository"
    )
    def test_connect_to_server_successful(
        self,
        encryption_service: MagicMock,
        uuid_generator: MagicMock,
        mock_client: MagicMock,
        member_repository: MagicMock,
    ):
        """Test succefull connection"""
        ip_address = "127.0.0.1"
        port = 1024
        guest = tuple(["127.0.0.1", 1111])
        auth_code = "auth_code"
        public_key = "public_key"
        uuid_generator.generate.return_value = auth_code
        mock_client.receive_message.side_effect = [
            tuple([public_key, guest]),
            tuple([auth_code, guest]),
        ]
        add_member_use_case = AddMember(
            uuid_generator, encryption_service, mock_client, member_repository
        )

        add_member_use_case.execute("abc", ip_address, port)

        mock_client.connect_to_server.assert_called_once_with(ip_address, port)

    @mock.patch(
        "src.application.interfaces.iasymetric_encryption_service",
        name="encryption_service",
    )
    @mock.patch(
        "src.application.interfaces.iid_generator_service", name="uuid_generator"
    )
    @mock.patch("src.application.interfaces.iclient_socket", name="mock_client")
    @mock.patch(
        "src.application.interfaces.imember_repository", name="member_repository"
    )
    def test_send_invitation(
        self,
        encryption_service: MagicMock,
        uuid_generator: MagicMock,
        mock_client: MagicMock,
        member_repository: MagicMock,
    ):
        """method to test send member invitation"""
        ip_address = "127.0.0.1"
        port = 1024
        guest = tuple(["127.0.0.1", 1111])
        auth_code = "auth_code"
        public_key = "public_key"
        uuid_generator.generate.return_value = auth_code
        mock_client.receive_message.side_effect = [
            tuple([public_key, guest]),
            tuple([auth_code, guest]),
        ]
        add_member_use_case = AddMember(
            uuid_generator, encryption_service, mock_client, member_repository
        )

        add_member_use_case.execute("abc", ip_address, port)

        mock_client.send_message.assert_any_call("invitation")

    @mock.patch(
        "src.application.interfaces.iasymetric_encryption_service",
        name="encryption_service",
    )
    @mock.patch(
        "src.application.interfaces.iid_generator_service", name="uuid_generator"
    )
    @mock.patch("src.application.interfaces.iclient_socket", name="mock_client")
    @mock.patch(
        "src.application.interfaces.imember_repository", name="member_repository"
    )
    def test_auth_key_generate(
        self,
        encryption_service: MagicMock,
        uuid_generator: MagicMock,
        mock_client: MagicMock,
        member_repository: MagicMock,
    ):
        """method to test add member to community"""
        ip_address = "127.0.0.1"
        port = 1024
        guest = tuple(["127.0.0.1", 1111])
        auth_code = "auth_code"
        public_key = "public_key"
        uuid_generator.generate.return_value = auth_code
        mock_client.receive_message.side_effect = [
            tuple([public_key, guest]),
            tuple([auth_code, guest]),
        ]
        add_member_use_case = AddMember(
            uuid_generator, encryption_service, mock_client, member_repository
        )

        add_member_use_case.execute("abc", ip_address, port)

        uuid_generator.generate.assert_called_once()

    @mock.patch(
        "src.application.interfaces.iasymetric_encryption_service",
        name="encryption_service",
    )
    @mock.patch(
        "src.application.interfaces.iid_generator_service", name="uuid_generator"
    )
    @mock.patch("src.application.interfaces.iclient_socket", name="mock_client")
    @mock.patch(
        "src.application.interfaces.imember_repository", name="member_repository"
    )
    def test_auth_key_not_same(
        self,
        encryption_service: MagicMock,
        uuid_generator: MagicMock,
        mock_client: MagicMock,
        member_repository: MagicMock,
    ):
        """method to test add member to community"""
        ip_address = "127.0.0.1"
        port = 1024
        guest = tuple(["127.0.0.1", 1111])
        public_key = "public_key"
        uuid_generator.generate.return_value = "auth_code"
        mock_client.receive_message.side_effect = [
            tuple([public_key, guest]),
            tuple(["other_auth_code", guest]),
        ]
        add_member_use_case = AddMember(
            uuid_generator, encryption_service, mock_client, member_repository
        )

        with pytest.raises(AuthentificationFailedError):
            add_member_use_case.execute("abc", ip_address, port)

    @mock.patch(
        "src.application.interfaces.iasymetric_encryption_service",
        name="encryption_service",
    )
    @mock.patch(
        "src.application.interfaces.iid_generator_service", name="uuid_generator"
    )
    @mock.patch("src.application.interfaces.iclient_socket", name="mock_client")
    @mock.patch(
        "src.application.interfaces.imember_repository", name="member_repository"
    )
    def test_add_member_to_community(
        self,
        encryption_service: MagicMock,
        uuid_generator: MagicMock,
        mock_client: MagicMock,
        member_repository: MagicMock,
    ):
        """method to test add member to community"""
        ip_address = "127.0.0.1"
        port = 1024
        guest = tuple(["127.0.0.1", 1111])
        auth_code = "auth_code"
        public_key = "public_key"
        uuid_generator.generate.return_value = auth_code
        mock_client.receive_message.side_effect = [
            tuple([public_key, guest]),
            tuple([auth_code, guest]),
        ]
        member = Member(auth_code, ip_address, port)
        community_id = "abc"

        add_member_use_case = AddMember(
            uuid_generator, encryption_service, mock_client, member_repository
        )

        add_member_use_case.execute(community_id, ip_address, port)

        member_repository.add_member_to_community.assert_called_once_with(
            community_id, member
        )

    @mock.patch(
        "src.application.interfaces.iasymetric_encryption_service",
        name="encryption_service",
    )
    @mock.patch(
        "src.application.interfaces.iid_generator_service", name="uuid_generator"
    )
    @mock.patch("src.application.interfaces.iclient_socket", name="mock_client")
    @mock.patch(
        "src.application.interfaces.imember_repository", name="member_repository"
    )
    def test_connection_closed(
        self,
        encryption_service: MagicMock,
        uuid_generator: MagicMock,
        mock_client: MagicMock,
        member_repository: MagicMock,
    ):
        """method to test add member to community"""
        ip_address = "127.0.0.1"
        port = 1024
        guest = tuple(["127.0.0.1", 1111])
        auth_code = "auth_code"
        public_key = "public_key"
        uuid_generator.generate.return_value = auth_code
        mock_client.receive_message.side_effect = [
            tuple([public_key, guest]),
            tuple([auth_code, guest]),
        ]

        add_member_use_case = AddMember(
            uuid_generator, encryption_service, mock_client, member_repository
        )

        add_member_use_case.execute("abc", ip_address, port)

        mock_client.close_connection.assert_called_once()
