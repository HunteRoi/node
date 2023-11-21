from unittest import mock
from unittest.mock import MagicMock
import pytest


from src.domain.entities.member import Member
from src.application.exceptions.authentification_failed_error import AuthentificationFailedError
from src.application.use_cases.add_member import AddMember


class TestAddMember:
    """Test add member to a community"""

    @mock.patch("src.application.interfaces.iencryption_asymetric_service",
                name="encryption_service")
    @mock.patch("src.application.interfaces.iid_generator_service", name="uuid_generator")
    @mock.patch("src.application.interfaces.iclient_socket", name="mock_client")
    @mock.patch("src.application.interfaces.imember_repository", name="member_repository")
    def test_connect_to_server_successful(self,
                                          encryption_service: MagicMock,
                                          uuid_generator: MagicMock,
                                          mock_client: MagicMock,
                                          member_repository: MagicMock):
        """Test succefull connection"""
        adress_ip = "127.0.0.1"
        port = 1234

        add_member_use_case = AddMember(uuid_generator,
                                        encryption_service,
                                        mock_client,
                                        member_repository)

        uuid_generator.generate.return_value = "auth_key"
        mock_client.receive_message.side_effect = [
            tuple(["public_key", tuple(["127.0.0.1", 1111])]),
            tuple(["auth_key", tuple(["127.0.0.1", 1111])])
        ]

        add_member_use_case.execute("abc", adress_ip, port)

        mock_client.connect_to_server.assert_called_once_with(adress_ip, port)

    @mock.patch("src.application.interfaces.iencryption_asymetric_service",
                name="encryption_service")
    @mock.patch("src.application.interfaces.iid_generator_service", name="uuid_generator")
    @mock.patch("src.application.interfaces.iclient_socket", name="mock_client")
    @mock.patch("src.application.interfaces.imember_repository", name="member_repository")
    def test_send_invitation(self,
                             encryption_service: MagicMock,
                             uuid_generator: MagicMock,
                             mock_client: MagicMock,
                             member_repository: MagicMock):
        """method to test send member invitation"""
        add_member_use_case = AddMember(uuid_generator,
                                        encryption_service,
                                        mock_client,
                                        member_repository)

        uuid_generator.generate.return_value = "auth_key"
        mock_client.receive_message.side_effect = [
            tuple(["public_key", tuple(["127.0.0.1", 1111])]),
            tuple(["auth_key", tuple(["127.0.0.1", 1111])])
        ]

        add_member_use_case.execute("abc", "127.0.0.1", 1234)

        mock_client.send_message.assert_any_call("invitation")

    @mock.patch("src.application.interfaces.iencryption_asymetric_service",
                name="encryption_service")
    @mock.patch("src.application.interfaces.iid_generator_service", name="uuid_generator")
    @mock.patch("src.application.interfaces.iclient_socket", name="mock_client")
    @mock.patch("src.application.interfaces.imember_repository", name="member_repository")
    def test_auth_key_generate(self,
                               encryption_service: MagicMock,
                               uuid_generator: MagicMock,
                               mock_client: MagicMock,
                               member_repository: MagicMock):
        """method to test add member to community"""
        add_member_use_case = AddMember(uuid_generator,
                                        encryption_service,
                                        mock_client,
                                        member_repository)

        uuid_generator.generate.return_value = "auth_key"
        mock_client.receive_message.side_effect = [
            tuple(["public_key", tuple(["127.0.0.1", 1111])]),
            tuple(["auth_key", tuple(["127.0.0.1", 1111])])
        ]

        add_member_use_case.execute("abc", "127.0.0.1", 1234)

        uuid_generator.generate.assert_called_once()

    @mock.patch("src.application.interfaces.iencryption_asymetric_service",
                name="encryption_service")
    @mock.patch("src.application.interfaces.iid_generator_service", name="uuid_generator")
    @mock.patch("src.application.interfaces.iclient_socket", name="mock_client")
    @mock.patch("src.application.interfaces.imember_repository", name="member_repository")
    def test_auth_key_not_same(self,
                               encryption_service: MagicMock,
                               uuid_generator: MagicMock,
                               mock_client: MagicMock,
                               member_repository: MagicMock):
        """method to test add member to community"""
        add_member_use_case = AddMember(uuid_generator,
                                        encryption_service,
                                        mock_client,
                                        member_repository)

        uuid_generator.generate.return_value = "auth_key"
        mock_client.receive_message.side_effect = [
            tuple(["public_key", tuple(["127.0.0.1", 1111])]),
            tuple(["auth_key_invalid", tuple(["127.0.0.1", 1111])])
        ]

        with pytest.raises(AuthentificationFailedError):
            add_member_use_case.execute("abc", "127.0.0.1", 1234)

    @mock.patch("src.application.interfaces.iencryption_asymetric_service",
                name="encryption_service")
    @mock.patch("src.application.interfaces.iid_generator_service", name="uuid_generator")
    @mock.patch("src.application.interfaces.iclient_socket", name="mock_client")
    @mock.patch("src.application.interfaces.imember_repository", name="member_repository")
    def test_add_member_to_community(self,
                                     encryption_service: MagicMock,
                                     uuid_generator: MagicMock,
                                     mock_client: MagicMock,
                                     member_repository: MagicMock):
        """method to test add member to community"""
        add_member_use_case = AddMember(uuid_generator,
                                        encryption_service,
                                        mock_client,
                                        member_repository)

        uuid_generator.generate.return_value = "auth_key"
        mock_client.receive_message.side_effect = [
            tuple(["public_key", tuple(["127.0.0.1", 1111])]),
            tuple(["auth_key", tuple(["127.0.0.1", 1111])])
        ]

        add_member_use_case.execute("abc", "127.0.0.1", 1234)

        member = Member("auth_key", "127.0.0.1")
        member_repository.add_member_to_community.assert_called_once_with(
            "abc", member)

    @mock.patch("src.application.interfaces.iencryption_asymetric_service",
                name="encryption_service")
    @mock.patch("src.application.interfaces.iid_generator_service", name="uuid_generator")
    @mock.patch("src.application.interfaces.iclient_socket", name="mock_client")
    @mock.patch("src.application.interfaces.imember_repository", name="member_repository")
    def test_connection_closed(self,
                               encryption_service: MagicMock,
                               uuid_generator: MagicMock,
                               mock_client: MagicMock,
                               member_repository: MagicMock):
        """method to test add member to community"""
        add_member_use_case = AddMember(uuid_generator,
                                        encryption_service,
                                        mock_client,
                                        member_repository)

        uuid_generator.generate.return_value = "auth_key"
        mock_client.receive_message.side_effect = [
            tuple(["public_key", tuple(["127.0.0.1", 1111])]),
            tuple(["auth_key", tuple(["127.0.0.1", 1111])])
        ]

        add_member_use_case.execute("abc", "127.0.0.1", 1234)

        mock_client.close_connection.assert_called_once()
