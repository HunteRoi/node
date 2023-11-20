from src.infrastructure.services.encryption_asymetric_service import EncryptionAsymetricService


class TestEncryptionAsymetricService:
    """Test Encryption Service"""

    def test_generate_asymetric_key_pair(self):
        """Test generate asymetric key pair"""

        encription_service = EncryptionAsymetricService()

        public_key, private_key = encription_service.generate_asymetric_key_pair()

        assert public_key is not None
        assert private_key is not None

    def test_convert_public_key_to_string(self):
        """Test convert public key to string PEM"""

        encription_service = EncryptionAsymetricService()

        public_key, _ = encription_service.generate_asymetric_key_pair()

        public_key_string = encription_service._convert_public_key_to_string(
            public_key)

        assert public_key_string is not None

    def test_convert_public_key_string_to_public_key(self):
        """Test convert public key string to public key"""

        encription_service = EncryptionAsymetricService()

        public_key, _ = encription_service.generate_asymetric_key_pair()

        public_key_string = encription_service._convert_public_key_to_string(
            public_key)

        public_key_bis = encription_service._convert_public_key_string_to_public_key(
            public_key_string)

        assert public_key == public_key_bis

    def test_asymetric_key_encryption_and_decryption(self):
        """Test asymetric key encryption"""

        encription_service = EncryptionAsymetricService()

        public_key, private_key = encription_service.generate_asymetric_key_pair()

        plaintext = "Hello, it's me"

        encrypted_data = encription_service.asymetric_key_encryption(
            plaintext, public_key)
        decrypted_data = encription_service.asymetric_key_decryption(
            encrypted_data, private_key)

        assert plaintext == decrypted_data

    def test_calcul_hash(self):
        """Test calcul hash"""

        encription_service = EncryptionAsymetricService()

        plaintext = "Hello, it's me"

        hash = encription_service.calcul_hash(plaintext)

        assert hash is not None
