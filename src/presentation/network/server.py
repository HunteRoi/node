import socket
from threading import Thread

from src.application.exceptions.socket_error import SocketError
from src.application.interfaces.iserver_socket import IServerSocket
from src.presentation.network.client import Client


class Server(Thread, IServerSocket):
    """Server class"""

    def __init__(self, port: int):
        super().__init__()
        self.port = port

        try:
            self.server_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.running = False
        except socket.error as err:
            raise SocketError(f"Unable to create socket :{err}") from err

    def run(self):
        try:
            self.server_socket.bind(('', self.port))
            self.server_socket.listen(5)
        except socket.error as err:
            raise SocketError(f"Unable to run server :{err}") from err

        self.running = True
        while self.running:
            client_socket, sender = self.server_socket.accept()
            client = Client(client_socket)
            client.send_message("Hello from server", sender[0], sender[1])
            client.close_connection()

    def stop(self):
        self.running = False
        self.server_socket.close()
