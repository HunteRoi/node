import os

from src.application.interfaces.ifile_service import IFileService


class FileService(IFileService):
    """File service"""

    def read_file(self, path: str, with_binary_format: bool = False) -> str | bytes:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File {path} not found")

        open_format = "rb" if with_binary_format else "r"

        with open(path, open_format) as file:
            return file.read()

    def write_file(self, path: str, content: str | bytes) -> None:
        open_format = "wb" if isinstance(content, bytes) else "w"

        with open(path, open_format) as file:
            file.write(content)
