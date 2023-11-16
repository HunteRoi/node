import socket
import threading


class Server(threading.Thread):
    """Server class"""

    def __init__(self, ip, port):
        super().__init__()
        threading.Thread.__init__(self)
        self.port = port
        self.ip = ip
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.running = False
        self.lock = threading.Lock()

    def stop_server(self):
        """Stop server"""
        with self.lock:
            self.running = False
        print("Server stopped")
        self.server_socket.close()

    def run_client(self, client_socket):
        """Run client"""
        try:
            print(f"Connection of {self.ip}:{self.port}")
            # receive data
            data = client_socket.recv(2048)
            print("Client message : ", data)
            # send data to client
            response_to_client = "Bonjour comment vas tu ?"
            client_socket.send(response_to_client.encode())
        except Exception as e:
            print(f"Exception: {e}")

    def start_server(self):
        """Start server"""
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(10)
        self.running = True
        print(f"Server listen on {self.ip}:{self.port}")

        try:
            while self.running:
                print("Listening ...")
                (client_socket, _) = self.server_socket.accept()
                client_thread = threading.Thread(
                    target=self.run_client, args=(client_socket,))
                client_thread.start()
        except KeyboardInterrupt:
            print("Shutdown server")
        finally:
            self.stop_server()


if __name__ == "__main__":
    server = Server("127.0.0.1", 12345)
    server.start_server()
