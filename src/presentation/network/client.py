import socket

from src.application.exceptions.socket_error import SocketError
from src.application.interfaces.iclient_socket import IClientSocket


class Client(IClientSocket):
    "Client socket class"
    BUFFER_SIZE = 2048

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
        self, message: str, ip_address: str | None = None, port: int | None = None
    ):
        has_target_data = ip_address is not None and port is not None
        message_to_send = message
        try:
            while len(message_to_send) > 0:
                encoded_chunk = message_to_send[: Client.BUFFER_SIZE].encode()
                if has_target_data:
                    self.client_socket.sendto(encoded_chunk, (ip_address, port))
                else:
                    self.client_socket.send(encoded_chunk)
                message_to_send = message_to_send[Client.BUFFER_SIZE :]
        except socket.error as err:
            raise SocketError(f"Unable to send message :{err}") from err

    def receive_message(self) -> tuple[str, tuple[str, int]]:
        message, sender = self.client_socket.recvfrom(Client.BUFFER_SIZE)
        decoded_message = message.decode()
        if len(message) == Client.BUFFER_SIZE:
            while message:
                message, _ = self.client_socket.recvfrom(Client.BUFFER_SIZE)
                decoded_message = decoded_message + message.decode()

        return decoded_message, sender

    def close_connection(self):
        self.client_socket.close()
