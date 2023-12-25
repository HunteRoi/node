from unittest import mock
from unittest.mock import MagicMock
import pytest

from src.application.use_cases.create_community import CreateCommunity


class TestCreateCommunity:
    """Test suite around creating a community."""

    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        """Create a temporary folder for the test."""
        base_path = "test_community_repository"
        return str(tmp_path_factory.mktemp(base_path, True))

    @pytest.fixture(scope="function", autouse=True, name="create_community_mocks")
    @mock.patch(
        "src.application.interfaces.icommunity_repository",
        name="mock_community_repository",
    )
    @mock.patch(
        "src.application.interfaces.imember_repository", name="mock_member_repository"
    )
    @mock.patch(
        "src.application.interfaces.iidea_repository", name="mock_idea_repository"
    )
    @mock.patch(
        "src.application.interfaces.iopinion_repository", name="mock_opinion_repository"
    )
    @mock.patch(
        "src.application.interfaces.iid_generator_service", name="mock_id_generator"
    )
    @mock.patch(
        "src.application.interfaces.isymetric_encryption_service",
        name="mock_encryption_service",
    )
    @mock.patch(
        "src.application.interfaces.imachine_service", name="mock_machine_service"
    )
    @mock.patch("src.application.interfaces.ifile_service", name="mock_file_service")
    def create_create_community_usecase(
        self,
        mock_community_repository: MagicMock,
        mock_member_repository: MagicMock,
        mock_idea_repository: MagicMock,
        mock_opinion_repository: MagicMock,
        mock_id_generator: MagicMock,
        mock_encryption_service: MagicMock,
        mock_machine_service: MagicMock,
        mock_file_service: MagicMock,
        temp_folder,
    ) -> CreateCommunity:
        """Create a use case for creating a community."""
        return CreateCommunity(
            temp_folder,
            mock_community_repository,
            mock_member_repository,
            mock_idea_repository,
            mock_opinion_repository,
            mock_id_generator,
            mock_encryption_service,
            mock_machine_service,
            mock_file_service,
        )

    def test_create_community(
        self,
        create_community_mocks: CreateCommunity,
    ):
        """It should be possible to create a community, given a name and a description."""
        name = "Test Community"
        description = "This is a test community"

        create_community_mocks.execute(name, description)

        create_community_mocks.community_repository.add_community.assert_called_once()

    def test_create_community_should_add_member(
        self,
        create_community_mocks: CreateCommunity,
    ):
        """Creating a new community should add the creator as a member."""
        name = "Test Community"
        description = "This is a test community"

        create_community_mocks.execute(name, description)

        create_community_mocks.member_repository.add_member_to_community.assert_called_once()

    def test_get_current_user(self, create_community_mocks: CreateCommunity):
        """Creating a new community should get the current user."""
        name = "Test Community"
        description = "This is a test community"

        create_community_mocks.execute(name, description)

        create_community_mocks.machine_service.get_current_user.assert_called_once()

    def test_create_community_should_generate_symetric_key(
        self,
        create_community_mocks: CreateCommunity,
    ):
        """Creating a new community should generate a symetric key."""
        name = "Test Community"
        description = "This is a test community"

        create_community_mocks.execute(name, description)

        create_community_mocks.encryption_service.generate_key.assert_called_once()

    def test_create_community_should_save_symetric_key(
        self,
        create_community_mocks: CreateCommunity,
    ):
        """Creating a new community should save the symetric key."""
        name = "Test Community"
        description = "This is a test community"

        create_community_mocks.execute(name, description)

        create_community_mocks.file_service.write_file.assert_called_once()

    def test_create_community_initialize_db(
        self,
        create_community_mocks: CreateCommunity,
    ):
        """Creating a community should initialize its requirements on other repositories."""
        create_community_mocks.execute("name", "description")

        create_community_mocks.community_repository.add_community.assert_called_once()
        create_community_mocks.member_repository.initialize_if_not_exists.assert_called_once()
        create_community_mocks.idea_repository.initialize_if_not_exists.assert_called_once()
        create_community_mocks.opinion_repository.initialize_if_not_exists.assert_called_once()

    def test_success_output(
        self,
        create_community_mocks: CreateCommunity,
    ):
        """Creating a community should return a success message."""
        output = create_community_mocks.execute("name", "description")

        assert output == "Success!"

    def test_error_output(
        self,
        create_community_mocks: CreateCommunity,
    ):
        """Creating a community should return an error message if an error occurs."""
        create_community_mocks.community_repository.add_community.side_effect = (
            Exception()
        )

        output = create_community_mocks.execute("name", "description")

        assert output != "Success!"
