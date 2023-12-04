from unittest import mock
from unittest.mock import mock_open, MagicMock
import pytest

from src.infrastructure.services.file_service import FileService


class TestFileService:
    """Test file service"""

    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        """Create a temporary folder for the test."""
        base_path = "test_file_service"
        return str(tmp_path_factory.mktemp(base_path, True))

    @pytest.fixture(scope="function", autouse=True, name="file_name")
    def create_test_file_path(self, temp_folder) -> str:
        """Create the test file path in the temp folder."""
        file_name = "test_file_service.txt"
        return f"{temp_folder}/{file_name}"

    @mock.patch("builtins.open")
    @mock.patch("os.path.exists")
    def test_read_file_open(self, exists: MagicMock, open_mock: MagicMock, file_name):
        """Test reading a file."""
        mock_file = mock_open(open_mock, "test")
        exists.return_value = True

        file_service = FileService()
        file_service.read_file(file_name)

        mock_file.assert_called_once_with(file_name, "r")

    @mock.patch("builtins.open")
    @mock.patch("os.path.exists")
    def test_read_file_not_exists(
        self, exists: MagicMock, open_mock: MagicMock, temp_folder
    ):
        """Test reading a file."""
        mock_file = mock_open(open_mock, "test")
        mock_file.return_value.read.return_value = None
        exists.return_value = False

        file_service = FileService()

        with pytest.raises(FileNotFoundError):
            file_service.read_file(f"{temp_folder}/invalid_file")

    @mock.patch("builtins.open")
    @mock.patch("os.path.exists")
    def test_read_file_called(self, exists: MagicMock, open_mock: MagicMock, file_name):
        """Test reading a file."""
        mock_file = mock_open(open_mock, "test")
        mock_file.return_value.read.return_value = "test"
        exists.return_value = True

        file_service = FileService()

        file_service.read_file(file_name)

        mock_file().read.assert_called_once_with()

    @mock.patch("builtins.open")
    @mock.patch("os.path.exists")
    def test_read_file_binary_format(
        self, exists: MagicMock, open_mock: MagicMock, file_name
    ):
        """Test reading a file."""
        mock_file = mock_open(open_mock, b"test")
        mock_file.return_value.read.return_value = b"test"
        exists.return_value = True

        file_service = FileService()

        result = file_service.read_file(file_name, True)

        assert result == b"test"

    @mock.patch("builtins.open")
    @mock.patch("os.path.exists")
    def test_read_file(self, exists: MagicMock, open_mock: MagicMock, file_name):
        """Test reading a file."""
        mock_file = mock_open(open_mock, "test")
        mock_file.return_value.read.return_value = "test"
        exists.return_value = True

        file_service = FileService()

        result = file_service.read_file(file_name)

        assert result == "test"

    @mock.patch("builtins.open")
    def test_write_file_open(self, open_mock, file_name):
        """Test writing a file."""
        mock_file = mock_open(open_mock, "test")

        file_service = FileService()

        file_service.write_file(file_name, "test")

        mock_file.assert_called_once_with(file_name, "w")

    @mock.patch("builtins.open")
    def test_write_file_binary_format(self, open_mock, file_name):
        """Test writing a file."""
        mock_file = mock_open(open_mock, b"test")

        file_service = FileService()

        file_service.write_file(file_name, b"test")

        mock_file.assert_called_once_with(file_name, "wb")

    @mock.patch("builtins.open")
    def test_write_file(self, open_mock, file_name):
        """Test writing a file."""
        mock_file = mock_open(open_mock, "test")

        file_service = FileService()
        file_service.write_file(file_name, "test")

        mock_file().write.assert_called_once_with("test")
