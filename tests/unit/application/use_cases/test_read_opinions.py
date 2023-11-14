from unittest import mock
from unittest.mock import MagicMock
from datetime import datetime

from src.domain.entities.member import Member
from src.domain.entities.opinion import Opinion
from src.domain.entities.idea import Idea
from src.application.use_cases.read_opinions import ReadOpinions


class TestReadOpinions:
    """Unit test for the use case of reading the opinions on idea or opinion."""

    @mock.patch("src.application.interfaces.iopinion_repository", name="opinion_repository")
    def test_get_opinion_from_idea(self, opinion_repository: MagicMock):
        """Test reading the content of a community."""
        member = Member("1234", "name", "description")
        idea = Idea(1, "Text", member, datetime.now())
        opinion = Opinion(2, "Text", member, datetime.now(), idea)

        opinion_repository.get_opinions_by_parent.return_value = [opinion]

        use_case = ReadOpinions(opinion_repository)
        result = use_case.execute("1234", idea.identifier)

        opinion_repository.get_opinions_by_parent.assert_called_once_with(
            "1234", idea.identifier)
        assert opinion in result

    @mock.patch("src.application.interfaces.iopinion_repository", name="opinion_repository")
    def test_get_opinions_from_idea(self, opinion_repository: MagicMock):
        """Test reading the content of a community."""
        member = Member("1234", "name", "description")
        idea = Idea(1, "Text", member, datetime.now())
        opinion_1 = Opinion(2, "Text", member, datetime.now(), idea)
        opinion_2 = Opinion(3, "Text", member, datetime.now(), idea)

        opinion_repository.get_opinions_by_parent.return_value = [
            opinion_1,
            opinion_2
        ]

        use_case = ReadOpinions(opinion_repository)
        result = use_case.execute("1234", idea.identifier)

        opinion_repository.get_opinions_by_parent.assert_called_once_with(
            "1234", idea.identifier)
        assert result == [opinion_1, opinion_2]

    @mock.patch("src.application.interfaces.iopinion_repository", name="opinion_repository")
    def test_get_opinion_from_opinion(self, opinion_repository: MagicMock):
        """Test reading the content of a community."""
        member = Member("1234", "name", "description")
        idea = Idea(1, "Text", member, datetime.now())
        opinion = Opinion(2, "Text", member, datetime.now(), idea)
        child_opinion = Opinion(3, "Text", member, datetime.now(), opinion)

        opinion_repository.get_opinions_by_parent.return_value = [
            child_opinion
        ]

        use_case = ReadOpinions(opinion_repository)
        result = use_case.execute("1234", opinion.identifier)

        opinion_repository.get_opinions_by_parent.assert_called_once_with(
            "1234", opinion.identifier)
        assert child_opinion in result

    @mock.patch("src.application.interfaces.iopinion_repository", name="opinion_repository")
    def test_get_opinions_from_opinion(self, opinion_repository: MagicMock):
        """Test reading the content of a community."""
        member = Member("1234", "name", "description")
        idea = Idea(1, "Text", member, datetime.now())
        opinion = Opinion(2, "Text", member, datetime.now(), idea)
        child_opinion_1 = Opinion(3, "Text", member, datetime.now(), opinion)
        child_opinion_2 = Opinion(4, "Text", member, datetime.now(), opinion)

        opinion_repository.get_opinions_by_parent.return_value = [
            child_opinion_1, child_opinion_2]

        use_case = ReadOpinions(opinion_repository)
        result = use_case.execute("1234", opinion.identifier)

        opinion_repository.get_opinions_by_parent.assert_called_once_with(
            "1234", opinion.identifier)
        assert result == [child_opinion_1, child_opinion_2]
