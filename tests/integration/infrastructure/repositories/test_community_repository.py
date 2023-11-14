import os
import pytest

from src.domain.entities.community import Community
from src.infrastructure.repositories.community_repository import CommunityRepository
from src.application.exceptions.community_already_exists_error import CommunityAlreadyExistsError


class TestCommunityRepository:
    """Test suite for the CommunityRepository class"""

    @pytest.fixture(scope="function", autouse=True, name="community")
    def create_community(self) -> Community:
        """Create a community for the test."""
        community = Community("1234", "name", "description")
        return community

    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(self, tmp_path_factory: pytest.TempPathFactory) -> str:
        """Create a temporary folder for the test."""
        base_path = "test_community_repository"
        return str(tmp_path_factory.mktemp(base_path, True))

    def test_init_creates_index_db(self, temp_folder):
        """Test that initializing the repository creates the index database"""
        CommunityRepository(temp_folder)

        assert os.path.exists(f"{temp_folder}/index.sqlite")

    def test_add_community_twice_fails(self, temp_folder, community: Community):
        """Test that adding a community twice fails"""
        repository = CommunityRepository(temp_folder)
        repository.add_community(community, "abc")

        with pytest.raises(CommunityAlreadyExistsError):
            repository.add_community(community, "abc")

    def test_get_community_returns_none_if_not_found(self, temp_folder, community: Community):
        """Test that the get_community method returns None if the community is not found"""
        repository = CommunityRepository(temp_folder)

        actual_community = repository.get_community(community.identifier)

        assert actual_community is None

    def test_get_community_with_proper_values(self, temp_folder, community: Community):
        """Test that the created community has the right values"""
        repository = CommunityRepository(temp_folder)
        repository.add_community(community, "abc")

        actual_community = repository.get_community(community.identifier)

        assert actual_community == community

    def test_get_communities(self, temp_folder, community: Community):
        """Test that getting the communities returns them"""
        repository = CommunityRepository(temp_folder)
        second_community = Community("5678", "name2", "description2")
        repository.add_community(community, "abc")
        repository.add_community(second_community, "abc")

        actual_communities = repository.get_communities()

        assert len(actual_communities) == 2
        assert community.identifier in [
            value.identifier for value in actual_communities]
        assert second_community.identifier in [
            value.identifier for value in actual_communities]

    def test_get_authentication_key_for_community(self, temp_folder, community: Community):
        """Test that the get_member_auth_key_for_community method returns the right value"""
        repository = CommunityRepository(temp_folder)
        auth_key = "abc"
        repository.add_community(community, auth_key)

        actual_auth_key = repository.get_authentication_key_for_community(
            community.identifier
        )

        assert actual_auth_key == auth_key
