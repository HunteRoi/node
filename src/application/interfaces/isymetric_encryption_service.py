from abc import ABC, abstractmethod


class ISymetricEncryptionService(ABC):
    """Interface for symetric encryption service."""

    @abstractmethod
    def generate_key(self) -> str:
        """Generates ramdom symetric symetric key."""

    @abstractmethod
    def encrypt(self, plaintext: str, key: str) -> tuple[bytes, str, str]:
        """Encrypts plaintext using symetric key. Returns the nonce, tag and ciphertext."""

    @abstractmethod
    def decrypt(self, ciphertext: str, key: str, tag: str, nonce: bytes) -> str:
        """Decrypts ciphertext using symetric key, tag and nonce. Returns the plaintext."""
