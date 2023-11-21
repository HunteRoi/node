from unittest import mock
from unittest.mock import MagicMock

from src.presentation.network.server import Server


class TestServer:
    """Test Server class"""

    def test_init(self):
        """Validates the constructor of Server initializes the object"""
        server = Server(1234)

        assert server is not None

    def test_port_attribute(self):
        """Validates the attribute port of the server"""
        port = 12345

        server = Server(port)

        assert server.port == port

    @mock.patch("socket.socket")
    def test_server_socket_created(self, mock_socket: MagicMock):
        """Validates that the server socket is created"""
        server = Server(1234)

        assert server.server_socket == mock_socket.return_value

    def test_stop_server_running(self):
        """Test stop server"""
        server = Server(1234)

        server.running = True
        server.stop()

        assert not server.running

    @mock.patch("socket.socket")
    def test_stop_server_socket(self, mock_socket: MagicMock):
        """Test stop server"""
        server = Server(1234)

        server.stop()

        mock_socket.return_value.close.assert_called_once()
