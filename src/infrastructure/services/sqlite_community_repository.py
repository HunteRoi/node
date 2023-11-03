import sqlite3

from src.application.interfaces.icommunity_repository import ICommunityRepository
from src.domain.entities.community import Community
from src.application.exceptions.community_already_exists_error import CommunityAlreadyExistsError


class SqliteCommunityRepository(ICommunityRepository):
    """Sqlite implementation of the ICommunityRepository interface"""

    def __init__(self, base_path: str):
        self.base_path = base_path
        self._execute_statement(
            """CREATE TABLE IF NOT EXISTS communities (
                id TEXT CONSTRAINT communities_pk PRIMARY KEY, 
                name TEXT NOT NULL, 
                description TEXT, 
                creation_date DATE DEFAULT CURRENT_DATE 
            )"""
        )

    def _execute_statement(self, statement: str, parameters: tuple = ()) -> None:
        """Execute a statement on the index database"""
        try:
            with sqlite3.connect(f"{self.base_path}/index.sqlite") as index_connection:
                index_cursor = index_connection.cursor()
                index_cursor.execute(statement, parameters)
                index_connection.commit()
        except sqlite3.IntegrityError as error:
            if "UNIQUE constraint failed: communities.id" in str(error):
                raise CommunityAlreadyExistsError(error) from error

    def _execute_query(self, statement: str, parameters: tuple = ()) -> list:
        """Execute a query on the index database"""
        with sqlite3.connect(f"{self.base_path}/index.sqlite") as index_connection:
            index_cursor = index_connection.cursor()
            result = index_cursor.execute(statement, parameters)
            return result.fetchall()

    def add_community(self, community: Community) -> None:
        """Add a community to the repository"""
        connection = sqlite3.connect(
            f"{self.base_path}/{community.identifier}.sqlite")

        self._execute_statement(
            "INSERT INTO communities (id, name, description, creation_date) VALUES (?, ?, ?, ?)",
            (community.identifier, community.name,
             community.description, str(community.creation_date))
        )
        connection.close()

    def get_community(self, identifier: str) -> None | Community:
        """Get a community from the repository"""

        result = self._execute_query(
            """SELECT id AS identifier, 
            name, 
            description, 
            creation_date FROM communities 
            WHERE id = ?""",
            (identifier,)
        )

        if len(result) == 0:
            return None

        identifier, name, description, creation_date = result[0]

        return Community(identifier, name, description, creation_date)
