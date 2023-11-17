from unittest import mock
from unittest.mock import MagicMock

from src.application.use_cases.create_community import CreateCommunity


class TestCreateCommunity:
    """Test suite around creating a community."""

    @mock.patch("src.application.interfaces.icommunity_repository",
                name="mock_community_repository")
    @mock.patch("src.application.interfaces.imember_repository", name="mock_member_repository")
    @mock.patch("src.application.interfaces.iidea_repository", name="mock_idea_repository")
    @mock.patch("src.application.interfaces.iopinion_repository", name="mock_opinion_repository")
    @mock.patch("src.application.interfaces.iid_generator_service", name="mock_id_generator")
    @mock.patch("src.application.interfaces.imachine_service", name="mock_machine_service")
    def test_create_community(self,
                              mock_community_repository: MagicMock,
                              mock_member_repository: MagicMock,
                              mock_idea_repository: MagicMock,
                              mock_opinion_repository: MagicMock,
                              mock_id_generator: MagicMock,
                              mock_machine_service: MagicMock):
        """It should be possible to create a community, given a name and a description."""
        name = "Test Community"
        description = "This is a test community"
        use_case = CreateCommunity(
            mock_community_repository,
            mock_member_repository,
            mock_idea_repository,
            mock_opinion_repository,
            mock_id_generator,
            mock_machine_service
        )

        use_case.execute(name, description)

        mock_community_repository.add_community.assert_called_once()

    @mock.patch("src.application.interfaces.icommunity_repository",
                name="mock_community_repository")
    @mock.patch("src.application.interfaces.imember_repository", name="mock_member_repository")
    @mock.patch("src.application.interfaces.iidea_repository", name="mock_idea_repository")
    @mock.patch("src.application.interfaces.iopinion_repository", name="mock_opinion_repository")
    @mock.patch("src.application.interfaces.iid_generator_service", name="mock_id_generator")
    @mock.patch("src.application.interfaces.imachine_service", name="mock_machine_service")
    def test_create_community_should_add_member(self,
                                                mock_community_repository: MagicMock,
                                                mock_member_repository: MagicMock,
                                                mock_idea_repository: MagicMock,
                                                mock_opinion_repository: MagicMock,
                                                mock_id_generator: MagicMock,
                                                mock_machine_service: MagicMock):
        """Creating a new community should add the creator as a member."""
        name = "Test Community"
        description = "This is a test community"
        use_case = CreateCommunity(
            mock_community_repository,
            mock_member_repository,
            mock_idea_repository,
            mock_opinion_repository,
            mock_id_generator,
            mock_machine_service
        )

        use_case.execute(name, description)

        mock_member_repository.add_member_to_community.assert_called_once()

    @mock.patch("src.application.interfaces.icommunity_repository",
                name="mock_community_repository")
    @mock.patch("src.application.interfaces.imember_repository", name="mock_member_repository")
    @mock.patch("src.application.interfaces.iidea_repository", name="mock_idea_repository")
    @mock.patch("src.application.interfaces.iopinion_repository", name="mock_opinion_repository")
    @mock.patch("src.application.interfaces.iid_generator_service", name="mock_id_generator")
    @mock.patch("src.application.interfaces.imachine_service", name="mock_machine_service")
    def test_create_community_initialize_db(self,
                                            mock_community_repository: MagicMock,
                                            mock_member_repository: MagicMock,
                                            mock_idea_repository: MagicMock,
                                            mock_opinion_repository: MagicMock,
                                            mock_id_generator: MagicMock,
                                            mock_machine_service: MagicMock):
        """Creating a community should initialize its requirements on other repositories."""
        use_case = CreateCommunity(
            mock_community_repository,
            mock_member_repository,
            mock_idea_repository,
            mock_opinion_repository,
            mock_id_generator,
            mock_machine_service
        )

        use_case.execute("name", "description")

        mock_community_repository.add_community.assert_called_once()
        mock_member_repository.initialize_if_not_exists.assert_called_once()
        mock_idea_repository.initialize_if_not_exists.assert_called_once()
        mock_opinion_repository.initialize_if_not_exists.assert_called_once()
