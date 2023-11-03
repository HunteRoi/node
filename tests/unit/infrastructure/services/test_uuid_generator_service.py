from unittest import mock
from unittest.mock import MagicMock

from src.infrastructure.services.uuid_generator_service import UuidGeneratorService


class TestUuidGeneratorService:
    """Test the UuidGeneratorService."""

    @mock.patch('uuid.uuid4', return_value='1234')
    def test_generate(self, mock_uuid4: MagicMock):
        """Test generating a UUID."""
        service = UuidGeneratorService()

        identifier = service.generate()

        assert identifier == mock_uuid4.return_value
