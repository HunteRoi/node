from datetime import datetime
from src.infrastructure.repositories.common.sqlite_repository import SqliteRepository
from src.application.interfaces.iidea_repository import IIdeaRepository
from src.domain.entities.idea import Idea


class IdeaRepository(IIdeaRepository, SqliteRepository):
    """Idea repository"""

    def initialize_if_not_exists(self, target_database: str) -> None:
        self._execute_statement(
            target_database,
            """CREATE TABLE IF NOT EXISTS messages (
                identifier INTEGER CONSTRAINT messages_pk PRIMARY KEY AUTOINCREMENT,
                author TEXT NOT NULL REFERENCES nodes(authentication_key),
                content TEXT NOT NULL,
                parent_message INTEGER REFERENCES messages(identifier) ON DELETE CASCADE,
                creation_date DATETIME DEFAULT CURRENT_TIMESTAMP
            );"""
        )

    def add_idea_to_community(self, community_id: str, idea: Idea) -> None:
        self.initialize_if_not_exists(community_id)

        self._execute_statement(
            community_id,
            """INSERT INTO messages(
                content,
                creation_date,
                author,
                parent_message
            ) VALUES (?, ?, ?, ?);""",
            (idea.content, str(idea.creation_date),
             idea.author.authentication_key, None)
        )

    def get_ideas_by_community(self, community_id: str) -> list[Idea]:
        result = self._execute_query(
            community_id,
            """SELECT
                identifier,
                content,
                creation_date,
                author
            FROM messages
            WHERE parent_message IS NULL;"""
        )

        return [Idea(
            identifier,
            content,
            author,
            datetime.fromisoformat(creation_date)
        ) for identifier, content, creation_date, author in result]
