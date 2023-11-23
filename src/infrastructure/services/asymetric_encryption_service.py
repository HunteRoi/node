from typing import Literal
import rsa.key
import rsa.pkcs1
from rsa.key import PublicKey, PrivateKey

from src.application.interfaces.iasymetric_encryption_service import (
    IAsymetricEncryptionService,
)


class AsymetricEncryptionService(IAsymetricEncryptionService):
    """Asymetric Encryption Service"""

    def generate_keys(self) -> tuple[str, str]:
        public_key, private_key = rsa.key.newkeys(2048)
        public_key_str = self._convert_to_string(public_key)
        private_key_str = self._convert_to_string(private_key)

        return (public_key_str, private_key_str)

    def encrypt(self, plaintext: str, public_key: str) -> str:
        if plaintext is None or plaintext.strip() == "":
            raise ValueError("Plaintext cannot be empty", plaintext)

        if public_key is None or public_key.strip() == "":
            raise ValueError("Public key cannot be empty", public_key)

        key = self._convert_to_key(public_key, "public")
        plaintext_bytes = plaintext.encode()

        ciphertext = rsa.pkcs1.encrypt(plaintext_bytes, key)
        return ciphertext.decode()

    def decrypt(self, ciphertext: str, private_key: str) -> str:
        if ciphertext is None or ciphertext.strip() == "":
            raise ValueError("Ciphertext cannot be empty", ciphertext)

        if private_key is None or private_key.strip() == "":
            raise ValueError("Private key cannot be empty", private_key)

        key = self._convert_to_key(private_key, "private")
        ciphertext_bytes = ciphertext.encode()

        return rsa.pkcs1.decrypt(ciphertext_bytes, key).decode()

    def _convert_to_string(self, key: PublicKey | PrivateKey) -> str:
        """Convert key object to string"""
        return key.save_pkcs1().decode()

    def _convert_to_key(
        self, key_string: str, key_type: Literal["public", "private"]
    ) -> PublicKey | PrivateKey:
        """Convert string to key object"""
        key_bytes = key_string.encode()

        if key_type == "public":
            return PublicKey.load_pkcs1(key_bytes)
        return PrivateKey.load_pkcs1(key_bytes)
