from src.application.interfaces.iread_communities import IReadCommunities
from src.application.interfaces.icommunity_repository import ICommunityRepository
from src.domain.entities.community import Community


class ReadCommunities(IReadCommunities):
    """Read communities use case implementation."""

    def __init__(self, community_repository: ICommunityRepository):
        self.community_repository = community_repository

    def execute(self) -> list[Community]:
        return self.community_repository.get_communities()
