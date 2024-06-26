import os
import pytest

from src.domain.entities.member import Member
from src.infrastructure.repositories.member_repository import MemberRepository
from src.application.exceptions.member_already_exists_error import (
    MemberAlreadyExistsError,
)


class TestMemberRepository:
    """Test suite for the MemberRepository class"""

    @pytest.fixture(scope="function", autouse=True, name="member")
    def create_member(self) -> Member:
        """Create a community for the test."""
        member = Member("abc", "127.0.0.1", 1024)
        return member

    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        """Create a temporary folder for the test."""
        base_path = "test_community_repository"
        return str(tmp_path_factory.mktemp(base_path, True))

    def test_add_member_to_community(self, temp_folder, member: Member):
        """Validates that it is possible to add a member to a community"""
        community_id = "1234"
        repository = MemberRepository(temp_folder)

        repository.add_member_to_community(community_id, member)

        assert os.path.exists(f"{temp_folder}/{community_id}.sqlite")

    def test_add_member_twice_fails(self, temp_folder, member: Member):
        """Test that adding a community twice fails"""
        repository = MemberRepository(temp_folder)
        repository.add_member_to_community("1234", member)

        with pytest.raises(MemberAlreadyExistsError):
            repository.add_member_to_community("1234", member)

    def test_get_member_from_community_returns_none_when_not_found(self, temp_folder):
        """Validates that None is returned when no member is found"""
        community_id = "1234"
        authentication_key = "abc"
        repository = MemberRepository(temp_folder)

        member = repository.get_member_for_community(community_id, authentication_key)

        assert member is None

    def test_get_member_from_community(self, temp_folder):
        """Validates that it is possible to get a member of a specific community"""
        community_id = "1234"
        authentication_key = "abc"
        member = Member(authentication_key, "127.0.0.1", 1024)
        repository = MemberRepository(temp_folder)
        repository.add_member_to_community(community_id, member)

        member = repository.get_member_for_community(community_id, authentication_key)

        assert member.authentication_key == authentication_key

    @pytest.mark.parametrize(
        "members",
        [
            [Member("abc", "127.0.0.1", 0)],
            [Member("abc", "127.0.0.1", 0), Member("abc2", "127.0.0.2", 0)],
            [
                Member("abc", "127.0.0.1", 0),
                Member("abc2", "127.0.0.2", 0),
                Member("abc3", "127.0.0.3", 0),
            ],
        ],
    )
    def test_get_members_from_community(self, temp_folder, members):
        """Validates that it is possible to get all members of a specific community"""
        community_id = "1234"
        repository = MemberRepository(temp_folder)
        for member in members:
            repository.add_member_to_community(community_id, member)

        actual_members = repository.get_members_from_community(community_id)

        assert len(actual_members) == len(members)

    def test_get_members_from_community_returns_empty_list_when_no_members(
        self, temp_folder
    ):
        """Validates that an empty list is returned when no members are found"""
        community_id = "1234"
        repository = MemberRepository(temp_folder)

        members = repository.get_members_from_community(community_id)

        assert len(members) == 0
