import os

from src.application.interfaces.icommunity_repository import ICommunityRepository
from src.application.interfaces.iid_generator_service import IIdGeneratorService
from src.infrastructure.services.sqlite_community_repository import SqliteCommunityRepository
from src.infrastructure.services.uuid_generator_service import UuidGeneratorService
from src.application.use_cases import create_community
from src.presentation.views.main_menu import MainMenu


class Application:
    """The application's entry point."""

    id_generator: IIdGeneratorService
    repository: ICommunityRepository
    create_community: create_community.CreateCommunity

    @staticmethod
    def run():
        """Configures the dependencies and runs the application."""
        Application._prepare()

        MainMenu(Application.create_community_usecase).show()

    @staticmethod
    def _prepare():
        os.makedirs(os.path.join(os.getcwd(), "data"), exist_ok=True)
        Application.id_generator = UuidGeneratorService()
        Application.repository = SqliteCommunityRepository(
            os.path.join(os.getcwd(), "data")
        )
        Application.create_community_usecase = create_community.CreateCommunity(
            Application.repository, Application.id_generator
        )
