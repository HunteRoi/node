from abc import ABC, abstractmethod


class IEncryptionSymetricService(ABC):
    """Interface for symetric encryption service."""

    @abstractmethod
    def generate_symetric_key(self) -> bytes:
        """Generate ramdom symetric symetric key"""

    @abstractmethod
    def symetric_key_encryption(self, plaintext: str, key: bytes) -> (bytes, bytes):
        """symetric key encryption."""

    @abstractmethod
    def symetric_key_decryption(self, ciphertext: bytes, key: bytes, iv: bytes) -> str:
        """symetric key decryption."""
