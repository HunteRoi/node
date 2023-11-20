from src.infrastructure.services.encryption_symetric_service import EncryptionSymetricService


class TestEncryptionSymetricService:

    def test_generate_symetric_key(self):
        """Test generate ramdom symetric  key"""

        encription_service = EncryptionSymetricService()

        key = encription_service.generate_symetric_key()

        assert key is not None

    def test_symetric_key_encryption_and_decryption(self):
        """Test symetric key encryption"""

        encription_service = EncryptionSymetricService()

        key = encription_service.generate_symetric_key()

        plaintext = "Hello, it's me"

        iv, encrypted_data = encription_service.symetric_key_encryption(
            plaintext, key)
        decrypted_data = encription_service.symetric_key_decryption(
            encrypted_data, key, iv)

        assert plaintext == decrypted_data

    def test_pad_data(self):
        """Test pad data"""

        encription_service = EncryptionSymetricService()

        plaintext = b"Hello, it's me"

        padded_data = encription_service._pad_data(plaintext)

        assert padded_data is not None
