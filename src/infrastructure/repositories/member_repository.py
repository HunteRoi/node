from datetime import datetime
import sqlite3

from src.infrastructure.repositories.common.sqlite_repository import SqliteRepository
from src.application.exceptions.member_already_exists_error import MemberAlreadyExistsError
from src.application.interfaces.imember_repository import IMemberRepository
from src.domain.entities.member import Member


class MemberRepository(IMemberRepository, SqliteRepository):
    """Sqlite implementation of the member repository class"""

    def _initialize_if_not_exists(self, target_database: str):
        self._execute_statement(
            target_database,
            """CREATE TABLE IF NOT EXISTS nodes (
                authentication_key TEXT CONSTRAINT nodes_pk PRIMARY KEY,
                ip_address TEXT NOT NULL,
                creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_connection_date DATE
            );"""
        )

    def add_member_to_community(self, community_id: str, member: Member) -> None:
        self._initialize_if_not_exists(community_id)

        try:
            self._execute_statement(
                community_id,
                """INSERT INTO nodes
                (authentication_key, ip_address, creation_date)
                VALUES (?, ?, ?);""",
                (member.authentication_key,
                 member.ip_address, str(member.creation_date))
            )
        except sqlite3.IntegrityError as error:
            if "UNIQUE constraint failed: nodes.authentication_key" in str(error):
                raise MemberAlreadyExistsError(error) from error

    def get_member_for_community(self, community_id: str, member_auth_key: str) -> Member | None:
        self._initialize_if_not_exists(community_id)

        result = self._execute_query(
            community_id,
            """SELECT
            authentication_key,
            ip_address,
            creation_date,
            last_connection_date
            FROM nodes WHERE authentication_key = ?;""",
            (member_auth_key,)
        )

        if len(result) == 0:
            return None

        authentication_key, ip_address, creation_date, last_connection_date = result[0]
        return Member(
            authentication_key,
            ip_address,
            datetime.fromisoformat(creation_date),
            None if last_connection_date is None else datetime.fromisoformat(
                last_connection_date)
        )
