import socket

from src.application.exceptions.socket_error import SocketError
from src.application.interfaces.iserver_socket import IServerSocket
from src.presentation.network.client import Client
from src.application.interfaces.ijoin_community import IJoinCommunity


class Server(IServerSocket):
    """Server class"""

    def __init__(
        self,
        port: int,
        join_community_usecase: IJoinCommunity,
    ):
        super().__init__()
        self.port = port
        self.join_community_usecase = join_community_usecase

        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.running = False
        except socket.error as err:
            raise SocketError(f"Unable to create socket :{err}") from err

    def run(self):
        try:
            self.server_socket.settimeout(1)
            self.server_socket.bind(("", self.port))
            self.server_socket.listen(5)
        except socket.error as err:
            raise SocketError(f"Unable to run server :{err}") from err

        self.running = True
        while self.running:
            try:
                client_socket, _ = self.server_socket.accept()
                client = Client(client_socket)
                message, _ = client.receive_message()
                if message == "INVITATION":
                    self.join_community_usecase.execute(client)
                elif message.startswith("CREATE_IDEA"):
                    print(f"Received idea : {message.split('|')[1]}")
                elif message.startswith("CREATE_OPINION"):
                    print(f"Received opinion : {message.split('|')[1]}")
                client.close_connection()
            except socket.timeout:
                pass

        self.server_socket.close()

    def stop(self):
        self.running = False
