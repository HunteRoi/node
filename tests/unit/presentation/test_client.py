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

        client.connect_to_server("127.0.0.1", 1024)

        mock_socket.return_value.connect.assert_called_once_with(("127.0.0.1", 1024))

    @mock.patch("socket.socket")
    def test_connect_to_server_refused(self, mock_socket: MagicMock):
        """test connect to server refused"""
        client = Client()

        mock_socket.return_value.connect.side_effect = SocketError("Connection refused")
        with pytest.raises(SocketError):
            client.connect_to_server("127.0.0.1", 1024)

    @mock.patch("socket.socket")
    def test_send_message(self, mock_socket: MagicMock):
        """Test send messages"""
        client = Client()
        message = "Hello I am the client"

        client.send_message(message)
        mock_socket.return_value.send.assert_called_once_with((message).encode())

        client.close_connection()

    @mock.patch("socket.socket")
    def test_send_message_to(self, mock_socket: MagicMock):
        """Test send messages"""
        client = Client()
        message = "Hello I am the client"
        ip_adress = "127.0.0.1"
        port = 1024

        client.send_message(message, ip_adress, port)

        mock_socket.return_value.sendto.assert_called_once_with(
            (message).encode(), (ip_adress, port)
        )

    @mock.patch("socket.socket")
    def test_receive_message(self, mock_socket: MagicMock):
        """Test receive messages"""
        client = Client()

        mock_socket.return_value.recvfrom.return_value = (
            "Hello client".encode(),
            ("127.0.0.1", 1024),
        )

        client.receive_message()

        mock_socket.return_value.recvfrom.assert_called_once_with(2048)

    @mock.patch("socket.socket")
    def test_message_receive_message(self, mock_socket: MagicMock):
        """Test receive messages"""
        client = Client()
        message = "Hello client"
        sender = ("127.0.0.1", 1024)

        mock_socket.return_value.recvfrom.return_value = (message.encode(), sender)

        message_received, _ = client.receive_message()

        assert message_received == message

    @mock.patch("socket.socket")
    def test_sender_receive_message(self, mock_socket: MagicMock):
        """Test receive messages"""
        client = Client()
        message = "Hello client"
        sender = ("127.0.0.1", 1024)

        mock_socket.return_value.recvfrom.return_value = (message.encode(), sender)

        _, received_sender = client.receive_message()

        assert received_sender == sender

    @mock.patch("socket.socket")
    def test_send_big_message_call_count(self, mock_socket: MagicMock):
        """Test send file"""
        client = Client()

        message = "1ef9704e5960f89dd0b22ce57e6eb89a8ae02ed32105588ef86b9df5f034184923c3f4f44b6561c12d890f6d9f4d7deecc78fa0bcc47f750d327c35b233bffd2bee85182f536dad966e0a45c006535e0071fc815bf92c06b353f35c29ddd4a556e339017bb6696eea5fa41b313a400f435630d7fae27bd9f9058b5cec1d1f096d394f354162f89dc754b078d2a40656c773dd4f234a496fe41290364c3e1c3b1c3774d963cbfbd303fcb3226ee8bd5648ab874fb820f34b0449d1d8b72fb50b8b14f7632ec7dd098a6b37aeb9bcd414bb7e6a4a225ef28e6125b6262b7daf67d17aa19f48bdb41dd884c01b3bb8be1c0011a96325f8816dfc0f95704e16880f94b1b85beaae5377d6bd8d14bb24c439f4fc3b5593c9ba39eda5101b34c4d4ccdac28a9d955278276abaf14f2b01f4ac04f67443eb1729019d3ed97e56b06d0d7a133468a6e6253ffafcf795b24d083290f520bbe4962d3d30c65185265411a0cc21f23ab86226edca27354be2f6b854d2feb7e1e733b908840a78fd52fcd3a8cfc36ce18230d9531f328eda93bca5f581039d0d3ebb44f1a89b183ec1f4171c59d17662d8a4c425f2be46977ffa5bab9d1cfbd954f158d04d63444a56b28b4a6091b273659a9baa4ac414d7479ef022f74019a527ece6ae5c9002597bcf3eb119240b8a12eaf5a6b52e2fc034867d2f6179ac08c6587b25d60324916f75d982036490e3552198749507d9a2bfc1e3db60251b9ae9d9249410d8de54fa073033ddf82a4df607d005976561b85cd6d75965fabfd2c392d367ed2aa4548b0119f601f81cf3b85b268a81a98e3e46f1b5f9cb8816db994ec07a1c20704d02af7e5b96948d1af3a17226393f0976ffaa5fab4105b29c4ae4fa324dacc8f89af8b59c97a22eb59750e69f5f70f6f8a7ab279b6486074ce32f4ef6d6ee3dd295de10d27ee955990b3efe8648807bd1864c9da20b76d731bbe12c9129c796850c161e3fb7c879e4abe632848d5f82c10a70a7601bea26d2d89669fc381a87258d3f3be5268fc77c8e2d64e924300162479debeaae5aca45500ffa5490ce359ba358c5f4d0d6b6c6bceeb70104128eb0430ed49f3550473c14b1bf1196563484551fa3a03516c3a80eb6d1c1bb1a1b05720a5787a0aef46dad996da89e0a17d7b3c94587cd6992372726285bf6d7588dec4159b9ea9352fe0240a3afff2d92fede1b581f10a3548a49e7856415adc0411ca8216723567717a14ed89a7170f09b8fe5fec155721492c1b7164315dc325964441aeee849bb1faddc3e1c1293ddb9d5961086acde6db816dc6d549ba63ab66fa130e2cac327c4bf3a207b2c602f57a2a9e8cc53c0db2b6b8a65cf15e12191bca9d5d592d498e3c9d04e912cd69e3fe711f4411d3b075d7237c5a88d4c9363e6b68b3857f8a7606b68d2147d1953e91ca70e486f50fd3b6041e75ae23d1e4e9cff0a7dce618223c3224770dbf9b7e126aae18a06746be04ab09d27eafbf24e16b2ef309c3e721d94497452295a954a8a722644e4cb9afb485eb52e3516b1b43522dfe1f3a53db88e9cee81f0e493d35e4ce05e710f06690d5d3f50c5b5cbea956aa1691cfd04bc605c7f8897e7a623de17bbcadbdca01320adba02db84dcaa69a05f817a5aeee5fa4f7222ed46e5554390593de3f24d3769d3150a94055d7aaacec42d4e5934128d7ad54fbdc6d3edf94d84cfe67f71bbb65cde2db021969152fa8de95089cdbb5a682807e8d610d4ff0d9133103cb424b3da801a5990fb9a2da5530758cc37d88d9731422313b5b128d5efbd0f13116e7479a5297ef766e9de7a416a16fb79d586fee69a0a2a17ecb64a474d3ef44c808e02cc4afefd3e0aad26252a44d521378e6753c4e2efe3566a69b373c640c7775191cabe419d8e1e810dc180863ab2a80f37570b70273e1807f6cf0e0c837da9a5a24205de1978f88b5681ac23973afe16e94a11c1f3362c389ebfd35d6003e71f43b2297c07089c929ea5f682d9f0ab4dcff68b2392f9e8433cdeec098bb5c9defff465b790ec591b83b90d2056f573f9df9e8bc0b86a5ff874ea86b9412fa7d13fda074735c895189bf46603d893699dba518f40cf3e1de12d01a2ae35f49109101c227b5ee848463cee637b7f3cd6d802ecdfebbb3bc0348ba32089f293a7e2e405cde0c2520b70fdc7e8769c5f94cdc911dc6aabbb70c2a9ad309661cb597fb0f965d08b11a07419820d8290415580da80fbc24fd03ba35008a8417387cde2f93c4a26045b97377847361450a820fca8d11dc4816420e2d6831865b043eea444ab972df76e8cbee64de870090783dcda3630b2f67e400ed2d62aac6dd1643b10d0ea66db0426f79b37f4e658138abc2b490ddecb82a3002bbaa078361cb0966230241aa8774064ec0b30f948fbaf867a2f9d6ea1a8f2d9a0f16718b5195969d8b099afb173153e80ba6673833a7c16ccbdd10dfdc8e930fcc3bdb0d6be7154cd39bf79b7fd67a83ad51eedb05e80a6e668848bec8fe9cdeb7c9736132df3f4d1d7bfc95f8ae3e8d6bed6534d8e015f1e969d688afa5455afdaa55076386db05a8d4bb51475f96c2d21c1efb25cbcb20990f251db9d82b9ae9e5f3dca227862093b8563ed064278187982cd0175902dcc0ef04aa17c70bab4977a5dd79756fa7dcd33c63f03f07c8268b1cf4c297cf"

        client.send_message(message)

        assert mock_socket.return_value.send.call_count > 1

    @mock.patch("socket.socket")
    def test_receive_big_message(self, mock_socket: MagicMock):
        """Test receive big messages"""
        client = Client()
        sender = ("127.0.0.1", 1024)

        message_1 = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        message_2 = "bbbbb"

        mock_socket.return_value.recvfrom.side_effect = [
            (message_1.encode(), sender),
            (message_2.encode(), sender),
            ("".encode(), sender),
        ]

        message_received, _ = client.receive_message()

        assert message_received == message_1 + message_2

    @mock.patch("socket.socket")
    def test_receive_big_message_call_count(self, mock_socket: MagicMock):
        """Test receive big messages"""
        client = Client()
        sender = ("127.0.0.1", 1024)

        message_1 = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        message_2 = "bbbbb"

        mock_socket.return_value.recvfrom.side_effect = [
            (message_1.encode(), sender),
            (message_2.encode(), sender),
            ("".encode(), sender),
        ]

        client.receive_message()

        assert mock_socket.return_value.recvfrom.call_count > 1
