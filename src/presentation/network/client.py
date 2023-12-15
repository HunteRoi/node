import socket

from src.application.exceptions.socket_error import SocketError
from src.application.interfaces.iclient_socket import IClientSocket


class Client(IClientSocket):
    "Client socket class"

    def __init__(self, client_socket: socket.socket = None):
        try:
            if client_socket is not None:
                self.client_socket = client_socket
            else:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            raise SocketError(f"Unable to create socket :{err}") from err

    def connect_to_server(self, ip_adress: str, port: int):
        try:
            self.client_socket.connect((ip_adress, port))
        except socket.error as err:
            raise SocketError(f"Unable to connect to server :{err}") from err

    def send_message(
        self, message: str, ip_adress: str | None = None, port: int | None = None
    ):
        try:
            if ip_adress is not None and port is not None:
                self.client_socket.sendto(message.encode(), (ip_adress, port))
            else:
                self.client_socket.send(message.encode())
        except socket.error as err:
            raise SocketError(f"Unable to send message :{err}") from err

    def receive_message(self) -> tuple[str, tuple[str, int]]:
        message, sender = self.client_socket.recvfrom(2048)
        decoded_message = message.decode()
        return decoded_message, sender

    def close_connection(self):
        self.client_socket.close()
