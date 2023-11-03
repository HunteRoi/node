import os
import pytest

from src.domain.entities.community import Community
from src.infrastructure.services.sqlite_community_repository import SqliteCommunityRepository
from src.application.exceptions.community_already_exists_error import CommunityAlreadyExistsError


class TestSqliteCommunityRepository:
    """Test suite for the SqliteCommunityRepository class"""

    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(self, tmp_path_factory: pytest.TempPathFactory) -> str:
        """Create a temporary folder for the test."""
        base_path = "test_sqlite_community_repository"
        return str(tmp_path_factory.mktemp(base_path, True))

    def test_init_creates_index_db(self, temp_folder):
        """Test that initializing the repository creates the index database"""
        SqliteCommunityRepository(temp_folder)

        assert os.path.exists(f"{temp_folder}/index.sqlite")

    def test_add_community_inits_community_db(self, temp_folder):
        """Test that the add_community method creates a database for the community"""
        community = Community("1234", "name", "description")
        repository = SqliteCommunityRepository(temp_folder)

        repository.add_community(community)

        assert os.path.exists(f"{temp_folder}/{community.identifier}.sqlite")

    def test_add_community_twice_fails(self, temp_folder):
        """Test that adding a community twice fails"""
        repository = SqliteCommunityRepository(temp_folder)
        community = Community("1234", "name", "description")
        repository.add_community(community)

        with pytest.raises(CommunityAlreadyExistsError):
            repository.add_community(community)

    def test_get_community_returns_none_if_not_found(self, temp_folder):
        """Test that the get_community method returns None if the community is not found"""
        repository = SqliteCommunityRepository(temp_folder)

        actual_community = repository.get_community("1234")

        assert actual_community is None

    def test_get_community_with_proper_values(self, temp_folder):
        """Test that the created community has the right values"""
        repository = SqliteCommunityRepository(temp_folder)
        community = Community("1234", "name", "description")
        repository.add_community(community)

        actual_community = repository.get_community(community.identifier)

        assert actual_community.identifier == community.identifier
        assert actual_community.name == community.name
        assert actual_community.description == community.description
