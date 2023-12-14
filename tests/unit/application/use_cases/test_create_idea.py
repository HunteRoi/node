from unittest import mock
from unittest.mock import MagicMock

from src.application.use_cases.create_idea import CreateIdea
from src.domain.entities.member import Member


class TestCreateIdea:
    """Test suite around creating an idea."""

    @mock.patch("src.application.interfaces.iidea_repository", name="idea_repo_mock")
    @mock.patch(
        "src.application.interfaces.iid_generator_service",
        name="id_generator_service_mock",
    )
    @mock.patch(
        "src.application.interfaces.imachine_service", name="machine_service_mock"
    )
    def test_create_idea(
        self,
        machine_service_mock: MagicMock,
        id_generator_service_mock: MagicMock,
        idea_repo_mock: MagicMock,
    ):
        """Creating an idea should be possible given the proper arguments."""
        content = "content"
        usecase = CreateIdea(
            machine_service_mock,
            id_generator_service_mock,
            idea_repository=idea_repo_mock,
        )

        idea = usecase.execute("1", content)

        assert idea is not None

    @mock.patch("src.application.interfaces.iidea_repository", name="idea_repo_mock")
    @mock.patch(
        "src.application.interfaces.iid_generator_service",
        name="id_generator_service_mock",
    )
    @mock.patch(
        "src.application.interfaces.imachine_service", name="machine_service_mock"
    )
    def test_create_idea_content_is_well_set(
        self,
        machine_service_mock: MagicMock,
        id_generator_service_mock: MagicMock,
        idea_repo_mock: MagicMock,
    ):
        """Creating an idea should be possible given the proper arguments."""
        content = "content"
        usecase = CreateIdea(
            machine_service_mock,
            id_generator_service_mock,
            idea_repository=idea_repo_mock,
        )

        idea = usecase.execute("1", content)

        assert idea.content == content

    @mock.patch("src.application.interfaces.iidea_repository", name="idea_repo_mock")
    @mock.patch(
        "src.application.interfaces.iid_generator_service",
        name="id_generator_service_mock",
    )
    @mock.patch(
        "src.application.interfaces.imachine_service", name="machine_service_mock"
    )
    def test_create_idea_author_is_current_user(
        self,
        machine_service_mock: MagicMock,
        id_generator_service_mock: MagicMock,
        idea_repo_mock: MagicMock,
    ):
        """Creating an idea should be possible given the proper arguments."""
        content = "content"
        author = Member("auth_key", "127.0.0.1", 0)
        machine_service_mock.get_current_user.return_value = author
        usecase = CreateIdea(
            machine_service_mock,
            id_generator_service_mock,
            idea_repository=idea_repo_mock,
        )

        idea = usecase.execute("1", content)

        assert idea.author == author

    @mock.patch("src.application.interfaces.iidea_repository", name="idea_repo_mock")
    @mock.patch(
        "src.application.interfaces.iid_generator_service",
        name="id_generator_service_mock",
    )
    @mock.patch(
        "src.application.interfaces.imachine_service", name="machine_service_mock"
    )
    def test_create_idea_calls_repository(
        self, machine_service_mock, id_generator_service_mock, idea_repo_mock
    ):
        """Creating an idea should be possible given the proper arguments."""
        content = "content"
        author = Member("auth_key", "127.0.0.1", 0)
        machine_service_mock.get_current_user.return_value = author
        usecase = CreateIdea(
            machine_service_mock,
            id_generator_service_mock,
            idea_repository=idea_repo_mock,
        )

        idea = usecase.execute("1", content)

        idea_repo_mock.add_idea_to_community.assert_called_once_with("1", idea)
