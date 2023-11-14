import uuid

from src.application.interfaces.iid_generator_service import IIdGeneratorService


class UuidGeneratorService(IIdGeneratorService):
    """UUID generator service"""

    def generate(self) -> str:
        return str((uuid.uuid4()))
