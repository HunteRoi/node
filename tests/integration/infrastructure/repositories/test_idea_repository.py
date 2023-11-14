import os
from datetime import datetime
import pytest

from src.infrastructure.repositories.idea_repository import IdeaRepository
from src.domain.entities.member import Member
from src.domain.entities.idea import Idea


class TestIdeaRrepository:
    """Test suite for the IdeaRepository class"""

    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(self, tmp_path_factory: pytest.TempPathFactory) -> str:
        """Create a temporary folder for the test."""
        base_path = "test_idea_repository"
        return str(tmp_path_factory.mktemp(base_path, True))

    def test_add_idea_to_community(self, temp_folder):
        """Validates that it is possible to add an idea to a community"""
        community_id = "1234"
        member = Member("abc", "127.0.0.1")
        idea = Idea(1, "An idea", member, datetime.now())

        repository = IdeaRepository(temp_folder)

        repository.add_idea_to_community(community_id, idea)

        assert os.path.exists(f"{temp_folder}/{community_id}.sqlite")

    def test_get_ideas_by_community(self, temp_folder):
        """Validates that it is possible to get ideas by community"""
        community_id = "1234"
        member = Member("abc", "127.0.0.1")
        idea = Idea(1, "A first idea", member, datetime.now())
        idea2 = Idea(2, "A second idea", member, datetime.now())

        repository = IdeaRepository(temp_folder)

        repository.add_idea_to_community(community_id, idea)
        repository.add_idea_to_community(community_id, idea2)
        result = repository.get_ideas_by_community(community_id)

        assert len(result) == 2
        assert idea.identifier in [value.identifier for value in result]
        assert idea2.identifier in [value.identifier for value in result]
