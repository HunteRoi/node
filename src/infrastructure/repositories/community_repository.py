from datetime import datetime
import sqlite3

from src.infrastructure.repositories.common.sqlite_repository import SqliteRepository
from src.application.exceptions.community_already_exists_error import (
    CommunityAlreadyExistsError,
)
from src.application.interfaces.icommunity_repository import ICommunityRepository
from src.domain.entities.community import Community


class CommunityRepository(ICommunityRepository, SqliteRepository):
    """Sqlite implementation of the ICommunityRepository interface"""

    index_database = "index"

    def __init__(self, base_path: str):
        super().__init__(base_path)
        self.initialize_if_not_exists(CommunityRepository.index_database)

    def initialize_if_not_exists(self, target_database: str):
        self._execute_statement(
            target_database,
            """CREATE TABLE IF NOT EXISTS communities (
                identifier TEXT CONSTRAINT communities_pk PRIMARY KEY ,
                name TEXT NOT NULL,
                description TEXT,
                creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                auth_key TEXT NOT NULL,
                encryption_key_path TEXT NOT NULL
            );""",
        )

    def add_community(
        self, community: Community, member_auth_key: str, encryption_key_path: str
    ) -> None:
        try:
            self._execute_statement(
                CommunityRepository.index_database,
                """INSERT INTO communities (
                    identifier,
                    name,
                    description,
                    creation_date,
                    auth_key,
                    encryption_key_path
                ) VALUES (?, ?, ?, ?, ?, ?);""",
                (
                    community.identifier,
                    community.name,
                    community.description,
                    str(community.creation_date),
                    member_auth_key,
                    encryption_key_path,
                ),
            )
        except sqlite3.IntegrityError as error:
            if "UNIQUE constraint failed: communities.identifier" in str(error):
                raise CommunityAlreadyExistsError(error) from error

    def get_community(self, community_id: str) -> None | Community:
        result = self._execute_query(
            CommunityRepository.index_database,
            """SELECT identifier,
            name,
            description,
            creation_date FROM communities
            WHERE identifier = ?;""",
            (community_id,),
        )

        if len(result) == 0:
            return None

        community_id, name, description, creation_date = result[0]
        community = Community(
            community_id, name, description, datetime.fromisoformat(creation_date)
        )

        return community

    def get_communities(self) -> list[Community]:
        result = self._execute_query(
            CommunityRepository.index_database,
            """SELECT identifier,
            name,
            description,
            creation_date FROM communities;""",
        )

        return [
            Community(
                community_id, name, description, datetime.fromisoformat(creation_date)
            )
            for community_id, name, description, creation_date in result
        ]

    def get_authentication_key_for_community(self, community_id: str) -> str:
        result = self._execute_query(
            CommunityRepository.index_database,
            """SELECT auth_key FROM communities WHERE identifier = ?;""",
            (community_id,),
        )

        if len(result) == 0:
            return None

        (auth_key,) = result[0]
        return auth_key

    def get_community_encryption_key_path(self, community_id: str) -> str:
        result = self._execute_query(
            CommunityRepository.index_database,
            """SELECT encryption_key_path FROM communities WHERE identifier = ?;""",
            (community_id,),
        )

        if len(result) == 0:
            return None

        (encryption_key_path,) = result[0]
        return encryption_key_path
