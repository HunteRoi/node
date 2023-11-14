from unittest import mock
from unittest.mock import MagicMock

from src.domain.entities.community import Community
from src.application.use_cases.read_communities import ReadCommunities


class TestReadAllCommunities:
    """Unit test for the use case of reading communities"""

    @mock.patch("src.application.interfaces.icommunity_repository", name="community_repository")
    def test_read_one_community(self, community_repository: MagicMock):
        """Test reading the content of a community."""
        community = Community("1234", "name", "description")
        community_repository.get_communities.return_value = [community]
        use_case = ReadCommunities(community_repository)

        result = use_case.execute()

        community_repository.get_communities.assert_called_once()
        assert community in result

    @mock.patch("src.application.interfaces.icommunity_repository", name="community_repository")
    def test_read_communities(self, community_repository: MagicMock):
        """Test reading the content of a community."""
        community_1 = Community("1234", "name", "description")
        community_2 = Community("2345", "name", "description")
        community_3 = Community("3456", "name", "description")
        community_repository.get_communities.return_value = [
            community_1,
            community_2,
            community_3,
        ]
        use_case = ReadCommunities(community_repository)

        result = use_case.execute()

        community_repository.get_communities.assert_called_once()
        assert result == [community_1, community_2, community_3]
