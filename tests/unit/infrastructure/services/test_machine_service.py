from unittest import mock
from unittest.mock import MagicMock
import pytest

from src.infrastructure.services.machine_service import MachineService


class TestMachineService:
    """Test machine service."""

    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        """Create a temporary folder for the test."""
        base_path = "test_file_service"
        return str(tmp_path_factory.mktemp(base_path, True))

    @pytest.fixture(scope="function", autouse=True, name="machine_service")
    @mock.patch(
        "src.application.interfaces.icommunity_repository", name="community_repository"
    )
    @mock.patch("src.application.interfaces.iid_generator_service", name="id_generator")
    @mock.patch(
        "src.application.interfaces.iasymetric_encryption_service", name="encryption"
    )
    @mock.patch("src.application.interfaces.ifile_service", name="file_service")
    def fixture_machine_service(
        self,
        community_repository: MagicMock,
        id_generator: MagicMock,
        encryption: MagicMock,
        file_service: MagicMock,
        temp_folder,
    ) -> MachineService:
        """Fixture for machine service."""
        return MachineService(
            temp_folder, community_repository, id_generator, encryption, file_service
        )

    @mock.patch("socket.gethostbyname", name="socket")
    def test_get_ip_address_exists(
        self,
        socket: MagicMock,
        machine_service: MachineService,
    ):
        """Test that the get_ip_address method exists."""
        socket.return_value = "127.0.0.1"

        ip_address = machine_service.get_ip_address()

        assert ip_address is not None

    @mock.patch("socket.gethostbyname", name="socket")
    def test_get_ip_address(
        self,
        socket: MagicMock,
        machine_service: MachineService,
    ):
        """Test getting the IP address."""
        ip_address_expected = "127.0.0.1"
        socket.return_value = ip_address_expected

        ip_address = machine_service.get_ip_address()

        assert ip_address == ip_address_expected

    def test_get_asymetric_encryption_keys_generate_called(
        self,
        machine_service: MachineService,
    ):
        """Test getting the asymetric encryption keys."""
        machine_service.file_service.read_file.side_effect = FileNotFoundError

        machine_service.encryption_service.generate_keys.return_value = (
            "public_key",
            "private_key",
        )

        machine_service.get_asymetric_key_pair()

        machine_service.encryption_service.generate_keys.assert_called_once()

    def test_get_asymetric_encryption_keys_not_already_exists(
        self,
        machine_service: MachineService,
    ):
        """Test getting the asymetric encryption keys."""
        machine_service.encryption_service.generate_keys.return_value = (
            "public_key",
            "private_key",
        )

        public_key, private_key = machine_service.get_asymetric_key_pair()

        assert public_key is not None
        assert private_key is not None

    def test_get_asymetric_encryption_keys_read_file_called(
        self,
        machine_service: MachineService,
        temp_folder,
    ):
        """Test getting the asymetric encryption keys."""
        machine_service.get_asymetric_key_pair()

        calls = [
            mock.call(f"{temp_folder}/encryption_key.pub"),
            mock.call(f"{temp_folder}/encryption_key"),
        ]
        machine_service.file_service.read_file.assert_has_calls(calls, any_order=True)

    def test_get_asymetric_encryption_keys_already_exists(
        self,
        machine_service: MachineService,
    ):
        """Test getting the asymetric encryption keys."""
        machine_service.file_service.read_file.side_effect = [
            "public_key",
            "private_key",
        ]

        public_key, private_key = machine_service.get_asymetric_key_pair()

        assert public_key == "public_key"
        assert private_key == "private_key"

    def test_get_auth_key_exists(
        self,
        machine_service: MachineService,
    ):
        """Test that the get_auth_key method exists."""
        machine_service.community_repository.get_authentication_key_for_community.return_value = (
            "abc"
        )

        auth_key = machine_service.get_auth_key("1234")

        assert auth_key is not None

    def test_get_auth_key_with_community(
        self,
        machine_service: MachineService,
    ):
        """Test getting the authentication key."""
        machine_service.community_repository.get_authentication_key_for_community.return_value = (
            "abc"
        )

        auth_key_found = machine_service.get_auth_key("1234")

        assert auth_key_found == "abc"

    def test_get_auth_key_without_community_exists(
        self,
        machine_service: MachineService,
    ):
        """Test getting the authentication key."""
        machine_service.id_generator_service.generate.return_value = "abc"

        auth_key_found = machine_service.get_auth_key(None)

        assert auth_key_found is not None

    def test_get_auth_key_without_community(
        self,
        machine_service: MachineService,
    ):
        """Test getting the authentication key."""
        machine_service.id_generator_service.generate.return_value = "abc"

        auth_key_found = machine_service.get_auth_key(None)

        assert auth_key_found == "abc"

    def test_get_port_exists(
        self,
        machine_service: MachineService,
    ):
        """Validates that getting an available port on the machine is possible."""
        port = machine_service.get_port()

        assert port is not None

    @pytest.mark.parametrize("community_id", ["1234", None])
    def test_get_current_user(
        self, machine_service: MachineService, community_id: str | None
    ):
        """Test getting the current user."""

        user = machine_service.get_current_user(community_id)

        assert user is not None

    @pytest.mark.parametrize("community_id", ["1234", None])
    @mock.patch(
        "src.infrastructure.services.machine_service",
        name="get_auth_key_mock",
        return_value="auth_key",
    )
    def test_get_current_user_auth_key(
        self,
        get_auth_key_mock: MagicMock,
        machine_service: MachineService,
        community_id: str | None,
    ):
        """Test getting the current user."""
        machine_service.get_auth_key = get_auth_key_mock

        user = machine_service.get_current_user(community_id)

        assert user.authentication_key == get_auth_key_mock.return_value

    @pytest.mark.parametrize("community_id", ["1234", None])
    @mock.patch(
        "src.infrastructure.services.machine_service",
        name="get_ip_address_mock",
        return_value="127.0.0.1",
    )
    def test_get_current_user_ip_address(
        self,
        get_ip_address_mock: MagicMock,
        machine_service: MachineService,
        community_id: str | None,
    ):
        """Test getting the current user."""
        machine_service.get_ip_address = get_ip_address_mock

        user = machine_service.get_current_user(community_id)

        assert user.ip_address == get_ip_address_mock.return_value

    @pytest.mark.parametrize("community_id", ["1234", None])
    @mock.patch(
        "src.infrastructure.services.machine_service",
        name="get_port_mock",
        return_value=1234,
    )
    def test_get_current_user_port(
        self,
        get_port_mock: MagicMock,
        machine_service: MachineService,
        community_id: str | None,
    ):
        """Test getting the current user."""
        machine_service.get_port = get_port_mock

        user = machine_service.get_current_user(community_id)

        assert user.port == get_port_mock.return_value
