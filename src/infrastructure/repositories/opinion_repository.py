from datetime import datetime
from src.infrastructure.repositories.common.sqlite_repository import SqliteRepository
from src.application.interfaces.iopinion_repository import IOpinionRepository
from src.domain.entities.opinion import Opinion


class OpinionRepository(IOpinionRepository, SqliteRepository):
    """Opinion repository"""

    def initialize_if_not_exists(self, target_database: str):
        self._execute_statement(
            target_database,
            """CREATE TABLE IF NOT EXISTS messages (
                identifier TEXT CONSTRAINT messages_pk PRIMARY KEY,
                author TEXT NOT NULL REFERENCES nodes(authentication_key),
                content TEXT NOT NULL,
                parent_message TEXT REFERENCES messages(identifier) ON DELETE CASCADE,
                creation_date DATETIME DEFAULT CURRENT_TIMESTAMP
            );""",
        )

    def add_opinion_to_community(self, community_id: str, opinion: Opinion) -> None:
        self.initialize_if_not_exists(community_id)

        self._execute_statement(
            community_id,
            """INSERT INTO messages(
                identifier,
                content,
                creation_date,
                author,
                parent_message
            ) VALUES (?, ?, ?, ?, ?);""",
            (
                opinion.identifier,
                opinion.content,
                str(opinion.creation_date),
                opinion.author.authentication_key,
                opinion.parent.identifier,
            ),
        )

    def get_opinions_by_parent(
        self, community_id: str, parent_id: str
    ) -> list[Opinion]:
        result = self._execute_query(
            community_id,
            """SELECT
                identifier,
                content,
                creation_date,
                author,
                parent_message
            FROM messages
            WHERE parent_message = ?;""",
            (parent_id,),
        )

        return [
            Opinion(
                identifier,
                content,
                author,
                datetime.fromisoformat(creation_date),
                parent_message,
            )
            for identifier, content, creation_date, author, parent_message in result
        ]

    def get_opinion_from_community(
        self, community_id: str, opinion_id: str
    ) -> Opinion | None:
        result = self._execute_query(
            community_id,
            """SELECT
                identifier,
                content,
                creation_date,
                author,
                parent_message
            FROM messages
            WHERE identifier = ? AND parent_message IS NOT NULL;""",
            (opinion_id,),
        )

        if len(result) == 0:
            return None

        (identifier, content, creation_date, author, parent_message) = result[0]

        return Opinion(
            identifier,
            content,
            author,
            datetime.fromisoformat(creation_date),
            parent_message,
        )
