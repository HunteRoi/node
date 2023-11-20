from os import urandom
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives import padding

from src.application.interfaces.iencryption_symetric_service import IEncryptionSymetricService


class EncryptionSymetricService(IEncryptionSymetricService):
    """Encryption Symetric Service"""

    def generate_symetric_key(self) -> bytes:
        """Generate ramdom symetric symetric key"""
        key = get_random_bytes(16)

        return key

    def symetric_key_encryption(self, plaintext: str, key: bytes) -> (bytes, bytes):
        """symetric key encryption."""
        iv = urandom(16)  # Initialization Vector (IV) for AES
        plaintext_bytes = plaintext.encode('utf-8')

        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_data = self._pad_data(plaintext_bytes)
        ciphertext = cipher.encrypt(padded_data)

        return iv, ciphertext

    def symetric_key_decryption(self, ciphertext: bytes, key: bytes, iv: bytes) -> str:
        """symetric key decryption."""
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(ciphertext)
        unpadder = padding.PKCS7(AES.block_size).unpadder()
        plaintext_bytes = unpadder.update(decrypted_data) + unpadder.finalize()

        plaintext_str = plaintext_bytes.decode('utf-8')

        return plaintext_str

    def _pad_data(self, data: bytes) -> bytes:
        """Pad data using PKCS7 padding."""
        padder = padding.PKCS7(AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        return padded_data
