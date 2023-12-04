from abc import ABC, abstractmethod


class IFileService(ABC):
    """Interface for file service"""

    @abstractmethod
    def read_file(self, path: str, with_binary_format: bool = False) -> str | bytes:
        """Reads a file"""

    @abstractmethod
    def write_file(self, path: str, content: str | bytes) -> None:
        """Writes a file"""
