from datetime import datetime
from unittest import mock
from unittest.mock import MagicMock
import pytest

from src.application.use_cases.create_opinion import CreateOpinion
from src.domain.entities.idea import Idea
from src.domain.entities.member import Member
from src.domain.entities.opinion import Opinion


class TestCreateOpinion:
    """Test suite around creating an opinion."""

    @pytest.fixture(scope="function", autouse=True, name="author")
    def create_member(self):
        return Member("auth_key1", "127.0.0.1", 1664)

    @pytest.fixture(scope="function", autouse=True, name="create_opinion_usecase")
    @mock.patch("src.application.interfaces.ifile_service", name="file_service_mock")
    @mock.patch(
        "src.application.interfaces.isymetric_encryption_service",
        name="symetric_encryption_service_mock",
    )
    @mock.patch(
        "src.application.interfaces.icommunity_repository", name="community_repo_mock"
    )
    @mock.patch(
        "src.application.interfaces.imember_repository", name="member_repo_mock"
    )
    @mock.patch("src.application.interfaces.iidea_repository", name="idea_repo_mock")
    @mock.patch(
        "src.application.interfaces.iopinion_repository", name="opinion_repo_mock"
    )
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
        opinion_repo_mock: MagicMock,
        member_repo_mock: MagicMock,
        community_repo_mock: MagicMock,
        symetric_encryption_service_mock: MagicMock,
        file_service_mock: MagicMock,
    ):
        """Create a usecase instance."""
        return CreateOpinion(
            machine_service_mock,
            id_generator_service_mock,
            idea_repo_mock,
            opinion_repo_mock,
            member_repo_mock,
            community_repo_mock,
            symetric_encryption_service_mock,
            file_service_mock,
        )

    @pytest.fixture(scope="function", autouse=True, name="idea")
    def create_idea(self):
        """Create an idea instance."""
        return Idea("1", "content", Member("abc", "127.0.0.1", 1664))

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_create_opinion_calls_repository_for_idea(
        self, mock_client: MagicMock, create_opinion_usecase: CreateOpinion, idea: Idea
    ):
        """Creating an opinion should be possible given the proper arguments."""
        create_opinion_usecase.idea_repository.get_idea_from_community.return_value = (
            idea
        )

        create_opinion_usecase.execute("1", "1", "content")

        create_opinion_usecase.idea_repository.get_idea_from_community.assert_called_once()
        create_opinion_usecase.opinion_repository.get_opinion_from_community.assert_not_called()
        create_opinion_usecase.opinion_repository.add_opinion_to_community.assert_called_once()

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_create_opinion_calls_repository_for_opinion(
        self, mock_client: MagicMock, create_opinion_usecase: CreateOpinion, idea: Idea
    ):
        """Creating an opinion should be possible given the proper arguments."""
        create_opinion_usecase.idea_repository.get_idea_from_community.return_value = (
            None
        )
        create_opinion_usecase.opinion_repository.get_opinion_from_community.return_value = Opinion(
            "1", "content", Member("abc", "127.0.0.1", 1664), datetime.now(), idea
        )
        create_opinion_usecase.execute("1", "1", "content")

        create_opinion_usecase.idea_repository.get_idea_from_community.assert_called_once()
        create_opinion_usecase.opinion_repository.get_opinion_from_community.assert_called_once()
        create_opinion_usecase.opinion_repository.add_opinion_to_community.assert_called_once()

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
    def test_create_opinion_sends_opinion_to_other_members(
        self,
        mock_client: MagicMock,
        create_opinion_usecase: CreateOpinion,
        members: list[Member],
    ):
        """Creating an opinion should be possible given the proper arguments."""
        mock_client.return_value = mock_client
        author = members[0]
        create_opinion_usecase.id_generator_service.generate.return_value = "123"
        create_opinion_usecase.machine_service.get_current_user.return_value = author
        create_opinion_usecase.member_repository.get_members_from_community.return_value = (
            members
        )
        create_opinion_usecase.symetric_encryption_service.encrypt.return_value = (
            "nonce",
            "tag",
            "cipher",
        )

        create_opinion_usecase.execute("1", "1", "content")

        mock_client.send_message.assert_any_call("CREATE_OPINION|nonce,tag,cipher")
        assert mock_client.send_message.call_count == len(members) - 1

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_create_opinion_doesnt_send_opinion_when_no_members(
        self,
        mock_client: MagicMock,
        create_opinion_usecase: CreateOpinion,
        author: Member,
    ):
        """Creating an opinion should be possible given the proper arguments."""
        mock_client.return_value = mock_client
        content = "content"
        create_opinion_usecase.id_generator_service.generate.return_value = "123"
        create_opinion_usecase.machine_service.get_current_user.return_value = author

        create_opinion_usecase.execute("1", "1", content)

        mock_client.send_message.assert_not_called()

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
    def test_create_opinion_encrypts_data(
        self,
        mock_client: MagicMock,
        create_opinion_usecase: CreateOpinion,
        members: list[Member],
    ):
        """Creating an opinion should call the symetric encryption method"""
        mock_client.return_value = mock_client
        author = members[0]
        create_opinion_usecase.id_generator_service.generate.return_value = "123"
        create_opinion_usecase.machine_service.get_current_user.return_value = author
        create_opinion_usecase.member_repository.get_members_from_community.return_value = (
            members
        )

        create_opinion_usecase.execute("1", "1", "content")

        create_opinion_usecase.symetric_encryption_service.encrypt.assert_called()

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
    def test_create_opinion_reads_symetric_key_file(
        self,
        mock_client: MagicMock,
        create_opinion_usecase: CreateOpinion,
        members: list[Member],
    ):
        """Creating an opinion should call the symetric encryption method"""
        mock_client.return_value = mock_client
        author = members[0]
        create_opinion_usecase.id_generator_service.generate.return_value = "123"
        create_opinion_usecase.machine_service.get_current_user.return_value = author
        create_opinion_usecase.member_repository.get_members_from_community.return_value = (
            members
        )

        create_opinion_usecase.execute("1", "1", "content")

        create_opinion_usecase.community_repository.get_community_encryption_key_path.assert_called_once()
        create_opinion_usecase.file_service.read_file.assert_called_once()

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_success_output(
        self, mock_client: MagicMock, create_opinion_usecase: CreateOpinion
    ):
        """Creating an opinion should return a success output."""
        mock_client.return_value = mock_client

        output = create_opinion_usecase.execute("1", "1", "content")

        assert output == "Success!"

    @mock.patch("src.presentation.network.client.Client", name="mock_client")
    def test_error_output(
        self, mock_client: MagicMock, create_opinion_usecase: CreateOpinion
    ):
        """Creating an opinion should return an error output."""
        mock_client.return_value = mock_client
        create_opinion_usecase.idea_repository.get_idea_from_community.side_effect = (
            Exception()
        )

        output = create_opinion_usecase.execute("1", "1", "content")

        assert output != "Success!"
