from abc import ABC, abstractmethod
import sqlite3


class SqliteRepository(ABC):
    """Base class for all sqlite repositories"""

    def __init__(self, base_path: str):
        self.base_path = base_path

    def _execute_statement(self,
                           target_database: str,
                           statement: str,
                           parameters: tuple = ()) -> None:
        """Execute a statement on the target database"""

        with sqlite3.connect(f"{self.base_path}/{target_database}.sqlite") as index_connection:
            index_cursor = index_connection.cursor()
            index_cursor.execute(statement, parameters)
            index_connection.commit()

    def _execute_query(self,
                       target_database: str,
                       statement: str,
                       parameters: tuple = ()) -> list:
        """Execute a query on the target database"""
        with sqlite3.connect(f"{self.base_path}/{target_database}.sqlite") as index_connection:
            index_cursor = index_connection.cursor()
            result = index_cursor.execute(statement, parameters)
            return result.fetchall()

    @abstractmethod
    def _initialize_if_not_exists(self, target_database: str):
        """Initialize the related database if it does not exist"""
