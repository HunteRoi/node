from unittest import mock
from unittest.mock import MagicMock

from src.infrastructure.services.machine_service import MachineService


class TestMachineService:
    """Test machine service."""

    @mock.patch("socket.socket", name="socket")
    @mock.patch("src.application.interfaces.icommunity_repository", name="repository")
    @mock.patch("src.application.interfaces.iid_generator_service", name="id_generator")
    def test_get_ip_address_exists(self, socket: MagicMock, repository: MagicMock,
                                   id_generator: MagicMock):
        """Test that the get_ip_address method exists."""
        service = MachineService(repository, id_generator)

        socket.gethostbyname.return_value = "127.0.0.1"

        ip_address = service.get_ip_address()

        assert ip_address is not None

    @mock.patch("socket.gethostbyname", name="socket", return_value="127.0.0.1")
    @mock.patch("src.application.interfaces.icommunity_repository", name="repository")
    @mock.patch("src.application.interfaces.iid_generator_service", name="id_generator")
    def test_get_ip_address(self, socket: MagicMock, repository: MagicMock,  # pylint: disable=unused-argument
                            id_generator: MagicMock):
        """Test getting the IP address."""
        service = MachineService(repository, id_generator)

        ip_address = service.get_ip_address()

        assert ip_address == "127.0.0.1"

    @mock.patch("src.application.interfaces.icommunity_repository", name="repository")
    @mock.patch("src.application.interfaces.iid_generator_service", name="id_generator")
    def test_get_auth_key_exists(self, repository: MagicMock, id_generator: MagicMock):
        """Test that the get_auth_key method exists."""
        service = MachineService(repository, id_generator)
        repository.get_authentication_key_for_community.return_value = "abc"

        auth_key = service.get_auth_key("1234")

        assert auth_key is not None

    @mock.patch("src.application.interfaces.icommunity_repository", name="repository")
    @mock.patch("src.application.interfaces.iid_generator_service", name="id_generator")
    def test_get_auth_key_with_community(self, repository: MagicMock, id_generator: MagicMock):
        """Test getting the authentication key."""
        service = MachineService(repository, id_generator)
        repository.get_authentication_key_for_community.return_value = "abc"

        auth_key_found = service.get_auth_key("1234")

        assert auth_key_found == "abc"

    @mock.patch("src.application.interfaces.icommunity_repository", name="repository")
    @mock.patch("src.application.interfaces.iid_generator_service", name="id_generator")
    def test_get_auth_key_without_community_exists(self, repository: MagicMock,
                                                   id_generator: MagicMock):
        """Test getting the authentication key."""
        service = MachineService(repository, id_generator)
        id_generator.generate.return_value = "abc"

        auth_key_found = service.get_auth_key(None)

        assert auth_key_found is not None

    @mock.patch("src.application.interfaces.icommunity_repository", name="repository")
    @mock.patch("src.application.interfaces.iid_generator_service", name="id_generator")
    def test_get_auth_key_without_community(self, repository: MagicMock, id_generator: MagicMock):
        """Test getting the authentication key."""
        service = MachineService(repository, id_generator)
        id_generator.generate.return_value = "abc"

        auth_key_found = service.get_auth_key(None)

        assert auth_key_found == "abc"
