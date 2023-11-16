from unittest import mock
from unittest.mock import MagicMock

from src.presentation.network.server import Server


class TestServer:
    """Test Server class"""

    def test_init(self):
        """Validates the constructor of Server initializes the object"""
        server = Server("127.0.0.1", 12345)

        assert server is not None

    def test_ip_attribute(self):
        """Validates the attribute ip of the server"""
        ip = "127.0.0.1"

        server = Server(ip, 12345)

        assert server.ip == ip

    def test_port_attribute(self):
        """Validates the attribute port of the server"""
        port = 12345

        server = Server("127.0.0.1", port)

        assert server.port == port

    @mock.patch("socket.socket")
    def test_server_socket_created(self, mock_socket: MagicMock):
        """Validates that the server socket is created"""
        server = Server("127.0.0.1", 12345)

        assert server.server_socket == mock_socket.return_value

    @mock.patch("socket.socket")
    def test_stop_server(self, mock_socket: MagicMock):
        """Test stop server"""
        server = Server("127.0.0.1", 12345)

        server.stop_server()

        assert not server.running
        mock_socket.return_value.close.assert_called_once()

    @mock.patch("socket.socket")
    def test_run_client(self, mock_socket: MagicMock):
        """Test the run_client, which contains all the actions to be carried out with the client """
        server = Server("127.0.0.1", 12345)

        mock_socket.return_value.recv.return_value = "Hello, it's me"

        server.run_client(mock_socket.return_value)

        # 2048 is the buffer size of the recv method
        mock_socket.return_value.recv.assert_called_once_with(2048)
        mock_socket.return_value.send.assert_called_once()

    # This test is disabled because it is not possible to test the server.start_server method.
    # Indeed, this method has an infinite loop and therefore the test never ends.

    @mock.patch("socket.socket")
    @mock.patch("threading.Thread")
    def disabled_test_start_server(self, mock_socket: MagicMock, mock_thread: MagicMock):
        """Test start server"""
        server_ip = "127.0.0.1"
        server_port = 12345

        mock_socket.return_value.accept.return_value = (
            mock_socket.return_value,
            (server_ip, server_port)
        )

        server = Server(server_ip, server_port)

        server.start_server()

        mock_socket.assert_called_once_with()
        mock_socket.return_value.bind.assert_called_once_with(
            (server_ip, server_port))
        mock_socket.return_value.listen.assert_called_once_with(10)
        mock_socket.return_value.accept.assert_called_once()

        mock_thread.assert_called_once_with(
            server.run_client, (mock_socket.return_value,))
        mock_thread.return_value.start.assert_called_once()
