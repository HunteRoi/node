from abc import ABC, abstractmethod


class IAsymetricEncryptionService(ABC):
    """Interface for asymetric encryption service."""

    @abstractmethod
    def generate_keys(self) -> tuple[str, str]:
        """Generates a pair of private and public keys"""

    @abstractmethod
    def encrypt(self, plaintext: str, public_key: str) -> str:
        """Encrypts a plaintext with a key."""

    @abstractmethod
    def decrypt(self, ciphertext: str, private_key: str) -> str:
        """Decrypts a ciphertext with a key.
        If the encrypted data used a public key, you must use the
        corresponding private key to decrypt it."""
