import os
import pytest

from src.infrastructure.repositories.idea_repository import IdeaRepository
from src.domain.entities.member import Member
from src.domain.entities.idea import Idea


class TestIdeaRrepository:
    """Test suite for the IdeaRepository class"""

    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        """Create a temporary folder for the test."""
        base_path = "test_idea_repository"
        return str(tmp_path_factory.mktemp(base_path, True))

    @pytest.fixture(scope="function", autouse=True, name="author")
    def fixture_member(self):
        """Fixture for the author of the idea."""
        return Member("1234", "name", 1024)

    def test_add_idea_to_community(self, author: Member, temp_folder: str):
        """Validates that it is possible to add an idea to a community"""
        community_id = "1234"
        idea = Idea("1", "An idea", author)
        repository = IdeaRepository(temp_folder)

        repository.add_idea_to_community(community_id, idea)

        assert os.path.exists(f"{temp_folder}/{community_id}.sqlite")

    def test_get_ideas_by_community(self, author: Member, temp_folder: str):
        """Validates that it is possible to get ideas by community"""
        community_id = "1234"
        idea = Idea("1", "A first idea", author)
        idea2 = Idea("2", "A second idea", author)
        repository = IdeaRepository(temp_folder)
        repository.add_idea_to_community(community_id, idea)
        repository.add_idea_to_community(community_id, idea2)

        result = repository.get_ideas_by_community(community_id)

        assert len(result) == 2
        assert idea.identifier in [value.identifier for value in result]
        assert idea2.identifier in [value.identifier for value in result]

    def test_get_idea_from_community(self, author: Member, temp_folder: str):
        """Validates that it is possible to get an idea"""
        community_id = "1234"
        idea = Idea("1", "content", author)
        repository = IdeaRepository(temp_folder)
        repository.add_idea_to_community(community_id, idea)

        result = repository.get_idea_from_community(community_id, idea.identifier)

        assert result.identifier == idea.identifier
