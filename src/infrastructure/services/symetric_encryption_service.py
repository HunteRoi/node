import Crypto.Cipher.AES
import Crypto.Random

from src.application.interfaces.isymetric_encryption_service import (
    ISymetricEncryptionService,
)


class SymetricEncryptionService(ISymetricEncryptionService):
    """Symetric Encryption Service"""

    def generate_key(self) -> str:
        bytes_key = Crypto.Random.get_random_bytes(32)
        return bytes.hex(bytes_key)

    def encrypt(self, plaintext: str, key: str) -> tuple[str, str, str]:
        if plaintext is None or plaintext.strip() == "":
            raise ValueError("Plaintext cannot be empty", plaintext)

        if key is None or key.strip() == "":
            raise ValueError("Key cannot be empty", key)

        bytes_key = bytes.fromhex(key)
        plaintext_bytes = plaintext.encode()
        cipher = Crypto.Cipher.AES.new(bytes_key, Crypto.Cipher.AES.MODE_EAX)

        ciphertext, tag = cipher.encrypt_and_digest(plaintext_bytes)

        return (cipher.nonce.hex(), tag.hex(), ciphertext.hex())

    def decrypt(self, ciphertext: str, key: str, tag: str, nonce: str) -> str:
        if ciphertext is None or ciphertext.strip() == "":
            raise ValueError("Ciphertext cannot be empty", ciphertext)

        if key is None or key.strip() == "":
            raise ValueError("Key cannot be empty", key)

        if tag is None or tag.strip() == "":
            raise ValueError("Tag cannot be empty", tag)

        if nonce is None or nonce.strip() == "":
            raise ValueError("Nonce cannot be empty", nonce)

        bytes_key = bytes.fromhex(key)
        bytes_ciphertext = bytes.fromhex(ciphertext)
        bytes_tag = bytes.fromhex(tag)
        bytes_nonce = bytes.fromhex(nonce)

        cipher = Crypto.Cipher.AES.new(
            bytes_key, Crypto.Cipher.AES.MODE_EAX, bytes_nonce
        )

        plaintext_bytes = cipher.decrypt_and_verify(bytes_ciphertext, bytes_tag)

        return plaintext_bytes.decode()
