from unittest import mock
from unittest.mock import MagicMock
from datetime import datetime

import pytest

from src.domain.entities.member import Member
from src.domain.entities.idea import Idea
from src.application.use_cases.read_ideas_from_community import ReadIdeasFromCommunity


class TestReadIdeasFromCommunity:
    """Unit test for the use case of reading the ideas of a community."""

    @pytest.fixture(scope="function", autouse=True, name="author")
    def fixture_author(self):
        """Fixture for the author of the idea."""
        return Member("1234", "name", 1024)

    @mock.patch("src.application.interfaces.iidea_repository", name="idea_repository")
    def test_get_idea_from_community(self, idea_repository: MagicMock, author: Member):
        """Test reading the content of a community."""
        idea = Idea(1, "Text", author, datetime.now())
        idea_repository.get_ideas_by_community.return_value = [idea]
        use_case = ReadIdeasFromCommunity(idea_repository)

        result = use_case.execute("1234")

        idea_repository.get_ideas_by_community.assert_called_once_with("1234")
        assert idea in result

    @mock.patch("src.application.interfaces.iidea_repository", name="idea_repository")
    def test_get_ideas_from_community(self, idea_repository: MagicMock, author: Member):
        """Test reading the content of a community."""
        idea_1 = Idea(1, "Text", author, datetime.now())
        idea_2 = Idea(2, "Text", author, datetime.now())
        idea_3 = Idea(3, "Text", author, datetime.now())
        idea_repository.get_ideas_by_community.return_value = [idea_1, idea_2, idea_3]
        use_case = ReadIdeasFromCommunity(idea_repository)

        result = use_case.execute("1234")

        idea_repository.get_ideas_by_community.assert_called_once_with("1234")
        assert result == [idea_1, idea_2, idea_3]
