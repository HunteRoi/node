import uuid

from src.application.interfaces.iid_generator_service import IIdGeneratorService


class UuidGeneratorService(IIdGeneratorService):
    """UUID generator service"""

    def generate(self) -> str:
        """Generates a UUID"""
        return str((uuid.uuid4()))
