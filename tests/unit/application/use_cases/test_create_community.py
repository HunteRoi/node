from unittest import mock
from unittest.mock import MagicMock

from src.application.use_cases.create_community import CreateCommunity


class TestCreateCommunity:
    """Test the CreateCommunity use case."""

    @mock.patch("src.application.interfaces.icommunity_repository",
                name="mock_community_repository")
    @mock.patch("src.application.interfaces.imember_repository", name="mock_member_repository")
    @mock.patch("src.application.interfaces.iid_generator_service", name="mock_id_generator")
    @mock.patch("src.application.interfaces.imachine_service", name="mock_machine_service")
    def test_create_community(self,
                              mock_community_repository: MagicMock,
                              mock_member_repository: MagicMock,
                              mock_id_generator: MagicMock,
                              mock_machine_service: MagicMock):
        """Test creating a new community."""
        name = "Test Community"
        description = "This is a test community"
        use_case = CreateCommunity(
            mock_community_repository,
            mock_member_repository,
            mock_id_generator,
            mock_machine_service
        )

        use_case.execute(name, description)

        mock_id_generator.generate.assert_called_once()
        mock_community_repository.add_community.assert_called_once()
        mock_member_repository.add_member_to_community.assert_called_once()

    @mock.patch("src.application.interfaces.icommunity_repository",
                name="mock_community_repository")
    @mock.patch("src.application.interfaces.imember_repository", name="mock_member_repository")
    @mock.patch("src.application.interfaces.iid_generator_service", name="mock_id_generator")
    @mock.patch("src.application.interfaces.imachine_service", name="mock_machine_service")
    def test_create_community_should_add_member(self,
                                                mock_community_repository: MagicMock,
                                                mock_member_repository: MagicMock,
                                                mock_id_generator: MagicMock,
                                                mock_machine_service: MagicMock):
        """Test creating a new community should add the creator as a member."""
        name = "Test Community"
        description = "This is a test community"
        use_case = CreateCommunity(
            mock_community_repository,
            mock_member_repository,
            mock_id_generator,
            mock_machine_service
        )

        use_case.execute(name, description)

        mock_machine_service.get_auth_key.assert_called_once()
        mock_machine_service.get_ip_address.assert_called_once()
        mock_member_repository.add_member_to_community.assert_called_once()
