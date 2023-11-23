from unittest import mock
from unittest.mock import MagicMock
import pytest

from src.infrastructure.services.asymetric_encryption_service import (
    AsymetricEncryptionService,
)


class TestAsymetricEncryptionService:
    """Test suite for the service of encryption with asymetric methods"""

    @pytest.fixture(scope="function", autouse=True, name="mock_public_key")
    def mock_public_key(self) -> MagicMock:
        """Mock public key"""
        public_key = "public_key"
        public_key_mock = mock.MagicMock(return_value=public_key)
        public_key_mock.save_pkcs1.return_value = public_key_mock
        public_key_mock.decode.return_value = public_key
        public_key_mock.encode.return_value = public_key
        return public_key_mock

    @pytest.fixture(scope="function", autouse=True, name="mock_private_key")
    def mock_private_key(self) -> MagicMock:
        """Mock private key"""
        private_key = "private_key"
        private_key_mock = mock.MagicMock(return_value=private_key)
        private_key_mock.save_pkcs1.return_value = private_key_mock
        private_key_mock.decode.return_value = private_key
        return private_key_mock

    @mock.patch("rsa.key", name="mock_rsa_key")
    def test_generate_keys(
        self,
        mock_rsa_key: MagicMock,
        mock_public_key: MagicMock,
        mock_private_key: MagicMock,
    ):
        """Validates that it is possible to generate a pair of keys"""
        mock_rsa_key.newkeys.return_value = (mock_public_key, mock_private_key)
        service = AsymetricEncryptionService()

        received_public_key, received_private_key = service.generate_keys()

        assert received_public_key == mock_public_key.return_value
        assert received_private_key == mock_private_key.return_value

    @pytest.mark.parametrize("plaintext, public_key", [("", "key"), (None, "key")])
    def test_encrypt_raises_value_error_with_empty_text(
        self,
        plaintext: str,
        public_key: str,
    ):
        """Validates that it is not possible to encrypt an empty text"""
        service = AsymetricEncryptionService()

        with pytest.raises(ValueError):
            service.encrypt(plaintext, public_key)

    @pytest.mark.parametrize("plaintext, public_key", [("text", ""), ("text", None)])
    def test_encrypt_raises_value_error_with_empty_pubkey(
        self,
        plaintext: str,
        public_key: str,
    ):
        """Validates that it is not possible to encrypt with an empty public key"""
        service = AsymetricEncryptionService()

        with pytest.raises(ValueError):
            service.encrypt(plaintext, public_key)

    @pytest.mark.parametrize(
        "plaintext, public_key, encrypted_data", [("text", "key", "encrypted_data")]
    )
    @mock.patch("rsa.key.PublicKey.load_pkcs1", name="mock_rsa_public_key_loader")
    @mock.patch("rsa.pkcs1.encrypt", name="mock_rsa_encrypt")
    def test_encrypt(
        self,
        mock_rsa_encrypt: MagicMock,
        mock_rsa_public_key_loader: MagicMock,
        plaintext: str,
        public_key: str,
        encrypted_data: str,
    ):
        """Validates that it is possible to encrypt a text if the parameters are valid"""
        mock_rsa_public_key_loader.return_value = public_key
        mock_rsa_encrypt.return_value = mock_rsa_encrypt
        mock_rsa_encrypt.decode.return_value = encrypted_data
        service = AsymetricEncryptionService()

        received_encrypted_data = service.encrypt(plaintext, public_key)

        assert received_encrypted_data == encrypted_data

    @pytest.mark.parametrize("ciphertext, private_key", [("", "key"), (None, "key")])
    def test_decrypt_raises_value_error_with_empty_text(
        self,
        ciphertext: str,
        private_key: str,
    ):
        """Validates that it is not possible to decrypt an empty text"""
        service = AsymetricEncryptionService()

        with pytest.raises(ValueError):
            service.decrypt(ciphertext, private_key)

    @pytest.mark.parametrize("ciphertext, private_key", [("text", ""), ("text", None)])
    def test_decrypt_raises_value_error_with_empty_privkey(
        self,
        ciphertext: str,
        private_key: str,
    ):
        """Validates that it is not possible to decrypt with an empty private key"""
        service = AsymetricEncryptionService()

        with pytest.raises(ValueError):
            service.decrypt(ciphertext, private_key)

    @pytest.mark.parametrize(
        "ciphertext, private_key, decrypted_data", [("text", "key", "decrypted_data")]
    )
    @mock.patch("rsa.key.PrivateKey.load_pkcs1", name="mock_rsa_private_key_loader")
    @mock.patch("rsa.pkcs1.decrypt", name="mock_rsa_decrypt")
    def test_decrypt(
        self,
        mock_rsa_decrypt: MagicMock,
        mock_rsa_private_key_loader: MagicMock,
        ciphertext: str,
        private_key: str,
        decrypted_data: str,
    ):
        """Validates that it is possible to decrypt a text if the parameters are valid"""
        mock_rsa_private_key_loader.return_value = private_key
        mock_rsa_decrypt.return_value = mock_rsa_decrypt
        mock_rsa_decrypt.decode.return_value = decrypted_data
        service = AsymetricEncryptionService()

        received_decrypted_data = service.decrypt(ciphertext, private_key)

        assert received_decrypted_data == decrypted_data
