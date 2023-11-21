from unittest import mock
from unittest.mock import MagicMock
import pytest

from src.presentation.network.client import Client
from src.application.exceptions.socket_error import SocketError


class TestClient:
    """Test Client class"""

    def test_init_client(self):
        """Test init client"""
        client = Client()

        assert client is not None

    @mock.patch("socket.socket")
    def test_client_socket(self, mock_socket: MagicMock):
        """Test init client"""
        client = Client(mock_socket)

        assert client.client_socket is not None

    @mock.patch("socket.socket")
    def test_connect_to_server(self, mock_socket: MagicMock):
        """Test succefull connection"""
        client = Client()

        mock_socket.return_value.connect.return_value = None

        client.connect_to_server("127.0.0.1", 1234)

        mock_socket.return_value.connect.assert_called_once_with(
            ("127.0.0.1", 1234))

    @mock.patch("socket.socket")
    def test_connect_to_server_refused(self, mock_socket: MagicMock):
        """test connect to server refused"""
        client = Client()

        mock_socket.return_value.connect.side_effect = SocketError(
            "Connection refused")
        with pytest.raises(SocketError):
            client.connect_to_server("127.0.0.1", 1234)

    @mock.patch("socket.socket")
    def test_send_message(self, mock_socket: MagicMock):
        """Test send messages"""
        client = Client()
        message = "Hello I am the client"

        client.send_message(message)
        mock_socket.return_value.send.assert_called_once_with(
            (message).encode())

        client.close_connection()

    @mock.patch("socket.socket")
    def test_send_message_to(self, mock_socket: MagicMock):
        """Test send messages"""
        client = Client()
        message = "Hello I am the client"
        ip_adress = "127.0.0.1"
        port = 1234

        client.send_message(message, ip_adress, port)

        mock_socket.return_value.sendto.assert_called_once_with(
            (message).encode(), (ip_adress, port))

    @mock.patch("socket.socket")
    def test_receive_message(self, mock_socket: MagicMock):
        """Test receive messages"""
        client = Client()

        mock_socket.return_value.recvfrom.return_value = ("Hello client".encode(),
                                                          ("127.0.0.1", 1234))

        client.receive_message()

        mock_socket.return_value.recvfrom.assert_called_once_with(2048)

    @mock.patch("socket.socket")
    def test_message_receive_message(self, mock_socket: MagicMock):
        """Test receive messages"""
        client = Client()
        message = "Hello client"
        sender = ("127.0.0.1", 1234)

        mock_socket.return_value.recvfrom.return_value = (
            message.encode(), sender)

        message_received, _ = client.receive_message()

        assert message_received == message

    @mock.patch("socket.socket")
    def test_sender_receive_message(self, mock_socket: MagicMock):
        """Test receive messages"""
        client = Client()
        message = "Hello client"
        sender = ("127.0.0.1", 1234)

        mock_socket.return_value.recvfrom.return_value = (
            message.encode(), sender)

        _, received_sender = client.receive_message()

        assert received_sender == sender
