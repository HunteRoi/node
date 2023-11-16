import socket


class Client:
    "Client class"

    def __init__(self, ip_server, port_number):
        self.ip_server = ip_server
        self.port_number = port_number
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self) -> bool:
        """Connect to server"""
        try:
            self.client_socket.connect((self.ip_server, self.port_number))
            return True
        except Exception:
            print("Connection refused by server")
            return False

    def send_messages(self, message):
        """Send messages"""
        try:
            self.client_socket.send(message.encode())
        except ConnectionRefusedError as connection_refused_error:
            print("The connection with the server has been lost: ",
                  connection_refused_error)
        except Exception as e:
            print(f"An unexpected error occurred while sending message: {e}")

    def receive_messages(self):
        """Receive messages"""
        msg = self.client_socket.recv(2048)
        decode_msg = msg.decode('utf-8')
        print(f"Server: {decode_msg}")
        return decode_msg

    def close_connection(self):
        """Close connection"""
        self.client_socket.close()
        print("Connection closed")

    def start_client(self):
        """Start client"""
        try:
            self.connect_to_server()
            if self.client_socket:
                message = input("Enter a message to send to the server: ")
                self.send_messages(message)
                self.receive_messages()
                self.close_connection()
        except KeyboardInterrupt as e:
            print("Error : ", e)


if __name__ == "__main__":
    client = Client("127.0.0.1", 12345)
    client.start_client()
