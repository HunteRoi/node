from abc import ABC, abstractmethod
from Crypto.PublicKey import RSA


class IEncryptionAsymetricService(ABC):
    """Interface for asymetric encryption service."""

    @abstractmethod
    def generate_asymetric_key_pair(self) -> (RSA.RsaKey, RSA.RsaKey):
        """Generate symetric key key pair"""

    @abstractmethod
    def asymetric_key_encryption(self, plaintext: str, public_key: RSA.RsaKey) -> bytes:
        """asymetric key  encryption"""

    @abstractmethod
    def asymetric_key_decryption(self, encrypted_data: bytes, private_key: RSA.RsaKey) -> str:
        """asymetric key decryption"""

    @abstractmethod
    def calcul_hash(self, data: str) -> str:
        """Calculate hash"""
