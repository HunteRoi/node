import base64
import rsa
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

from src.application.interfaces.iencryption_asymetric_service import IEncryptionAsymetricService


class EncryptionAsymetricService(IEncryptionAsymetricService):
    """Encryption Asymetric Service"""

    def generate_asymetric_key_pair(self) -> (RSA.RsaKey, RSA.RsaKey):
        """Generate symetric key key pair"""
        public_key, private_key = rsa.newkeys(2048)

        return public_key, private_key

    def _convert_public_key_to_string(self, public_key: RSA.RsaKey) -> str:
        """Convert public key to string PEM"""
        public_key_bytes = public_key.save_pkcs1(format='PEM')
        public_key_string = base64.b64encode(public_key_bytes).decode('utf-8')

        return public_key_string

    def _convert_public_key_string_to_public_key(self, public_key_string: str) -> RSA.RsaKey:
        """Convert public key string to public key"""
        public_key_bytes = base64.b64decode(public_key_string)
        public_key = rsa.PublicKey.load_pkcs1(public_key_bytes, format='PEM')

        return public_key

    def asymetric_key_encryption(self, plaintext: str, public_key: RSA.RsaKey) -> bytes:
        """asymetric key  encryption"""

        plaintext_bytes = plaintext.encode('utf-8')
        encrypted_data = rsa.encrypt(plaintext_bytes, public_key)

        return encrypted_data

    def asymetric_key_decryption(self, encrypted_data: bytes, private_key: RSA.RsaKey) -> str:
        """asymetric key decryption"""

        decrypted_data_bytes = rsa.decrypt(encrypted_data, private_key)
        decrypted_data_str = decrypted_data_bytes.decode('utf-8')

        return decrypted_data_str

    def calcul_hash(self, data: str) -> str:
        """Calculate hash"""
        data_bytes = data.encode('utf-8')
        data_hash = SHA256.new(data_bytes).hexdigest()

        return data_hash
