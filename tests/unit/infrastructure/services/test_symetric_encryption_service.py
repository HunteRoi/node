from unittest import mock
from unittest.mock import MagicMock

import pytest

from src.infrastructure.services.symetric_encryption_service import (
    SymetricEncryptionService,
)


class TestSymetricEncryptionService:
    """Test suite for the service of encryption with symetric methods"""

    @mock.patch("Crypto.Random.get_random_bytes", name="mock_get_random_bytes")
    def test_generate_key(self, mock_get_random_bytes: MagicMock):
        """Validates that it is possible to generate a key"""
        key = b"key"
        mock_get_random_bytes.return_value = key
        service = SymetricEncryptionService()

        received_key = service.generate_key()

        assert received_key is not None

    @pytest.mark.parametrize("plaintext, key", [("", "6b6579"), (None, "6b6579")])
    def test_encrypt_raises_value_error_with_empty_text(self, plaintext: str, key: str):
        """Validates that it is not possible to encrypt an empty text"""
        service = SymetricEncryptionService()

        with pytest.raises(ValueError):
            service.encrypt(plaintext, key)

    @pytest.mark.parametrize("plaintext, key", [("text", ""), ("text", None)])
    def test_encrypt_raises_value_error_with_empty_key(self, plaintext: str, key: str):
        """Validates that it is not possible to encrypt an empty text"""
        service = SymetricEncryptionService()

        with pytest.raises(ValueError):
            service.encrypt(plaintext, key)

    @pytest.mark.parametrize(
        "plaintext, key, ciphertext, tag, nonce",
        [("text", "6b6579", "cipher", "tag", b"nonce")],
    )
    @mock.patch("Crypto.Cipher.AES.new", name="mock_cipher")
    def test_encrypt(
        self,
        mock_cipher: MagicMock,
        plaintext: str,
        key: str,
        ciphertext: str,
        tag: str,
        nonce: bytes,
    ):
        """Validates that it is possible to encrypt a text"""
        mock_cipher.return_value = mock_cipher
        mock_cipher.encrypt_and_digest.return_value = (ciphertext, tag)
        mock_cipher.nonce = nonce
        service = SymetricEncryptionService()

        received_nonce, received_tag, received_ciphertext = service.encrypt(
            plaintext, key
        )

        assert received_nonce == nonce
        assert received_tag == tag
        assert received_ciphertext == ciphertext

    @pytest.mark.parametrize(
        "ciphertext, key, tag, nonce",
        [("", "6b6579", "tag", b"nonce"), (None, "6b6579", "tag", b"nonce")],
    )
    def test_decrypt_raises_value_error_with_empty_ciphertext(
        self, ciphertext: str, key: str, tag: str, nonce: bytes
    ):
        """Validates that it is not possible to decrypt an empty ciphertext"""
        service = SymetricEncryptionService()

        with pytest.raises(ValueError):
            service.decrypt(ciphertext, key, tag, nonce)

    @pytest.mark.parametrize(
        "ciphertext, key, tag, nonce",
        [("cipher", "", "tag", b"nonce"), ("cipher", None, "tag", b"nonce")],
    )
    def test_decrypt_raises_value_error_with_empty_key(
        self, ciphertext: str, key: str, tag: str, nonce: bytes
    ):
        """Validates that it is not possible to decrypt an empty key"""
        service = SymetricEncryptionService()

        with pytest.raises(ValueError):
            service.decrypt(ciphertext, key, tag, nonce)

    @pytest.mark.parametrize(
        "ciphertext, key, tag, nonce",
        [("cipher", "6b6579", "", b"nonce"), ("cipher", "6b6579", None, b"nonce")],
    )
    def test_decrypt_raises_value_error_with_empty_tag(
        self, ciphertext: str, key: str, tag: str, nonce: bytes
    ):
        """Validates that it is not possible to decrypt an empty tag"""
        service = SymetricEncryptionService()

        with pytest.raises(ValueError):
            service.decrypt(ciphertext, key, tag, nonce)

    @pytest.mark.parametrize(
        "ciphertext, key, tag, nonce",
        [("cipher", "6b6579", "tag", b""), ("cipher", "6b6579", "tag", None)],
    )
    def test_decrypt_raises_value_error_with_empty_nonce(
        self, ciphertext: str, key: str, tag: str, nonce: bytes
    ):
        """Validates that it is not possible to decrypt an empty nonce"""
        service = SymetricEncryptionService()

        with pytest.raises(ValueError):
            service.decrypt(ciphertext, key, tag, nonce)

    @pytest.mark.parametrize(
        "ciphertext, key, tag, nonce, plaintext",
        [("cipher", "6b6579", "tag", b"nonce", "text")],
    )
    @mock.patch("Crypto.Cipher.AES.new", name="mock_cipher")
    def test_decrypt(
        self,
        mock_cipher: MagicMock,
        ciphertext: str,
        key: str,
        tag: str,
        nonce: bytes,
        plaintext: str,
    ):
        """Validates that it is possible to decrypt a ciphertext"""
        mock_cipher.return_value = mock_cipher
        mock_cipher.decrypt_and_digest.return_value = mock_cipher
        mock_cipher.decode.return_value = plaintext
        service = SymetricEncryptionService()

        received_plaintext = service.decrypt(ciphertext, key, tag, nonce)

        assert received_plaintext == plaintext
