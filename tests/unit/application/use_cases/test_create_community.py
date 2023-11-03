from unittest import mock
from unittest.mock import MagicMock

from src.application.use_cases.create_community import CreateCommunity


class TestCreateCommunity:
    """Test the CreateCommunity use case."""

    @mock.patch("src.application.interfaces.icommunity_repository")
    @mock.patch("src.application.interfaces.iid_generator_service")
    def test_create_community(self, mock_repo: MagicMock, mock_id_generator: MagicMock):
        """Test creating a new community."""

        name = "Test Community"
        description = "This is a test community"
        use_case = CreateCommunity(mock_repo, mock_id_generator)

        use_case.execute(name, description)

        mock_id_generator.generate.assert_called_once()
        mock_repo.add_community.assert_called_once()
