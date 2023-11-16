from unittest import mock
from unittest.mock import MagicMock

from src.presentation.network.client import Client


class TestClient:
    """Test Client class"""

    def test_init_client(self):
        """Test init client"""
        client = Client("127.0.0.1", "1234")

        assert client is not None

    def test_ip_client(self):
        """Test ip client"""
        ip_address = "127.0.0.1"

        client = Client(ip_address, "1234")

        assert client.ip_server == ip_address

    def test_port_client(self):
        """Test last connection date client"""
        port = "1234"

        client = Client("127.0.0.1", port)

        assert client.port_number == port

    @mock.patch("socket.socket")
    def test_connect_to_server_successful(self, mock_socket: MagicMock):
        """Test succefull connection"""

        client = Client("127.0.0.1", 12345)
        mock_socket.return_value.connect.return_value = None
        connexion_status = client.connect_to_server()

        assert connexion_status is not False

    @mock.patch("socket.socket")
    def test_connect_to_server_refused(self, mock_socket: MagicMock):
        """test connect to server refused"""
        client = Client("127.0.0.1", 12345)

        mock_socket.return_value.connect.side_effect = Exception
        connexion_status = client.connect_to_server()

        assert connexion_status is False

    @mock.patch("socket.socket")
    def test_send_messages(self, mock_socket: MagicMock):
        """Test send messages"""
        client = Client("127.0.0.1", 12345)
        message = "Hello I am the client"

        client.send_messages(message)
        mock_socket.return_value.send.assert_called_once_with(
            (message).encode())

        client.close_connection()

    @mock.patch("socket.socket")
    def test_receive_messages(self, mock_socket: MagicMock):
        """Test receive messages"""
        client = Client("127.0.0.1", 12345)
        message = "Hello client"
        mock_socket.return_value.recv.return_value = message.encode()

        message_received = client.receive_messages()

        mock_socket.return_value.recv.assert_called_once_with(2048)

        assert message_received == message
