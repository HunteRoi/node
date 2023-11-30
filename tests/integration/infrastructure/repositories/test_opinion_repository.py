import os
from datetime import datetime
import pytest

from src.infrastructure.repositories.idea_repository import IdeaRepository
from src.infrastructure.repositories.opinion_repository import OpinionRepository
from src.domain.entities.opinion import Opinion
from src.domain.entities.member import Member
from src.domain.entities.idea import Idea


class TestOpinionRrepository:
    """Test suite for the OpinionRepository class"""

    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        """Create a temporary folder for the test."""
        base_path = "test_opinion_repository"
        return str(tmp_path_factory.mktemp(base_path, True))

    @pytest.fixture(scope="function", autouse=True, name="author")
    def fixture_member(self):
        """Fixture for the author of the idea."""
        return Member("1234", "name", 1024)

    def test_add_opinion_to_idea(self, author, temp_folder):
        """Validates that it is possible to add a opinion to a community"""
        community_id = "1234"
        idea = Idea(1, "An idea", author, datetime.now())
        opinion = Opinion(2, "An opinion", author, datetime.now(), idea)

        idea_repository = IdeaRepository(temp_folder)
        opinion_repository = OpinionRepository(temp_folder)

        idea_repository.add_idea_to_community(community_id, idea)
        opinion_repository.add_opinion_to_community(community_id, opinion)

        assert os.path.exists(f"{temp_folder}/{community_id}.sqlite")

    def test_get_opinions_by_parent(self, author, temp_folder):
        """Validates that it is possible to get a messages by message parent"""
        community_id = "1234"
        idea = Idea(1, "bienvenu", author, datetime.now())
        opinion = Opinion(2, "An opinion", author, datetime.now(), idea)

        idea_repository = IdeaRepository(temp_folder)
        opinion_repository = OpinionRepository(temp_folder)

        idea_repository.add_idea_to_community(community_id, idea)
        opinion_repository.add_opinion_to_community(community_id, opinion)

        result = opinion_repository.get_opinions_by_parent(
            community_id, idea.identifier
        )

        assert len(result) == 1
        assert result[0].identifier == opinion.identifier
        assert result[0].parent == opinion.parent.identifier
