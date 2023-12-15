from unittest import mock
from unittest.mock import MagicMock

import pytest

from src.presentation.network.server import Server


class TestServer:
    """Test Server class"""

    @pytest.fixture(scope="function", autouse=True, name="server")
    @mock.patch("src.application.interfaces.ijoin_community", name="join_community")
    def create_server(self, join_community: MagicMock) -> Server:
        """Create the server"""
        return Server(1234, join_community)

    def test_init(self, server: Server):
        """Validates the constructor of Server initializes the object"""
        assert server is not None

    def test_port_attribute(self, server: Server):
        """Validates the attribute port of the server"""
        port = 1234

        assert server.port == port

    def test_server_socket_created(self, server: Server):
        """Validates that the server socket is created"""

        assert server.server_socket is not None

    def test_stop_server_running(self, server: Server):
        """Test stop server"""
        server.running = True
        server.stop()

        assert not server.running

    def test_stop_server_socket(self, server: Server):
        """Test stop server"""
        server.running = True
        server.stop()

        assert not server.running
