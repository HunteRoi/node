from unittest import mock
from unittest.mock import MagicMock
import pytest

from src.application.use_cases.create_idea import CreateIdea
from src.domain.entities.member import Member


class TestCreateIdea:
    """Test suite around creating an idea."""

    @pytest.fixture(scope="function", autouse=True, name="create_idea_usecase")
    @mock.patch(
        "src.application.interfaces.isymetric_encryption_service",
        name="symetric_encryption_service_mock",
    )
    @mock.patch("src.application.interfaces.ifile_service", name="file_service_mock")
    @mock.patch(
        "src.application.interfaces.icommunity_repository", name="community_repo_mock"
    )
    @mock.patch(
        "src.application.interfaces.imember_repository", name="member_repo_mock"
    )
    @mock.patch("src.application.interfaces.iidea_repository", name="idea_repo_mock")
    @mock.patch(
        "src.application.interfaces.iid_generator_service",
        name="id_generator_service_mock",
    )
    @mock.patch(
        "src.application.interfaces.imachine_service", name="machine_service_mock"
    )
    def create_usecase(
        self,
        machine_service_mock: MagicMock,
        id_generator_service_mock: MagicMock,
        idea_repo_mock: MagicMock,
        member_repo_mock: MagicMock,
        community_repo_mock: MagicMock,
        file_service_mock: MagicMock,
        symetric_encryption_service_mock: MagicMock,
    ):
        """Create a usecase instance."""
        return CreateIdea(
            machine_service_mock,
            id_generator_service_mock,
            idea_repo_mock,
            member_repo_mock,
            community_repo_mock,
            file_service_mock,
            symetric_encryption_service_mock,
        )

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_create_idea_calls_repository(
        self, mock_client: MagicMock, create_idea_usecase: CreateIdea
    ):
        """Creating an idea should be possible given the proper arguments."""
        create_idea_usecase.execute("1", "content")

        create_idea_usecase.idea_repository.add_idea_to_community.assert_called_once()

    @pytest.mark.parametrize(
        "members",
        [
            [
                Member("auth_key1", "127.0.0.1", 1234),
                Member("auth_key2", "127.0.0.2", 1234),
            ],
            [
                Member("auth_key1", "127.0.0.1", 1234),
                Member("auth_key2", "127.0.0.2", 1234),
                Member("auth_key3", "127.0.0.3", 1234),
            ],
            [
                Member("auth_key1", "127.0.0.1", 1234),
                Member("auth_key2", "127.0.0.2", 1234),
                Member("auth_key3", "127.0.0.3", 1234),
                Member("auth_key4", "127.0.0.4", 1234),
            ],
        ],
    )
    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_create_idea_sends_idea_to_other_members(
        self,
        mock_client: MagicMock,
        create_idea_usecase: CreateIdea,
        members: list[Member],
    ):
        """Creating an idea should be possible given the proper arguments."""
        mock_client.return_value = mock_client
        author = members[0]
        create_idea_usecase.id_generator_service.generate.return_value = "123"
        create_idea_usecase.machine_service.get_current_user.return_value = author
        create_idea_usecase.member_repository.get_members_from_community.return_value = (
            members
        )
        create_idea_usecase.symetric_encryption_service.encrypt.return_value = (
            "nonce",
            "tag",
            "cipher",
        )

        create_idea_usecase.execute("1", "content")

        mock_client.send_message.assert_called()
        assert mock_client.send_message.call_count == len(members) - 1

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_create_idea_doesnt_send_idea_when_no_members(
        self, mock_client: MagicMock, create_idea_usecase: CreateIdea
    ):
        """Creating an idea should be possible given the proper arguments."""
        mock_client.return_value = mock_client
        content = "content"
        author = Member("auth_key1", "127.0.0.1", 1234)
        create_idea_usecase.id_generator_service.generate.return_value = "123"
        create_idea_usecase.machine_service.get_current_user.return_value = author

        create_idea_usecase.execute("1", content)

        mock_client.send_message.assert_not_called()

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_create_idea_reads_symetric_key_file(
        self, mock_client: MagicMock, create_idea_usecase: CreateIdea
    ):
        """Creating an idea should be possible given the proper arguments."""
        mock_client.return_value = mock_client
        content = "content"
        author = Member("auth_key1", "127.0.0.1", 1234)
        create_idea_usecase.id_generator_service.generate.return_value = "123"
        create_idea_usecase.machine_service.get_current_user.return_value = author

        create_idea_usecase.execute("1", content)

        create_idea_usecase.community_repository.get_community_encryption_key_path.assert_called_once()
        create_idea_usecase.file_service.read_file.assert_called_once()

    @pytest.mark.parametrize(
        "members",
        [
            [
                Member("auth_key1", "127.0.0.1", 1234),
                Member("auth_key2", "127.0.0.2", 1234),
            ],
            [
                Member("auth_key1", "127.0.0.1", 1234),
                Member("auth_key2", "127.0.0.2", 1234),
                Member("auth_key3", "127.0.0.3", 1234),
            ],
            [
                Member("auth_key1", "127.0.0.1", 1234),
                Member("auth_key2", "127.0.0.2", 1234),
                Member("auth_key3", "127.0.0.3", 1234),
                Member("auth_key4", "127.0.0.4", 1234),
            ],
        ],
    )
    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_create_idea_encrypts_data(
        self,
        mock_client: MagicMock,
        create_idea_usecase: CreateIdea,
        members: list[Member],
    ):
        """Creating an idea should be possible given the proper arguments."""
        mock_client.return_value = mock_client
        author = members[0]
        create_idea_usecase.id_generator_service.generate.return_value = "123"
        create_idea_usecase.machine_service.get_current_user.return_value = author
        create_idea_usecase.member_repository.get_members_from_community.return_value = (
            members
        )

        create_idea_usecase.execute("1", "content")

        create_idea_usecase.symetric_encryption_service.encrypt.assert_called()

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_success_output(
        self,
        mock_client: MagicMock,
        create_idea_usecase: CreateIdea,
    ):
        """Creating an idea should be possible given the proper arguments."""
        mock_client.return_value = mock_client

        output = create_idea_usecase.execute("1", "content")

        assert output == "Success!"

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_error_output(
        self,
        mock_client: MagicMock,
        create_idea_usecase: CreateIdea,
    ):
        """Creating an idea should be possible given the proper arguments."""
        mock_client.return_value = mock_client
        create_idea_usecase.id_generator_service.generate.side_effect = Exception()

        output = create_idea_usecase.execute("1", "content")

        assert output != "Success!"
