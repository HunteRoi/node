from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from src.application.interfaces.icreate_community import ICreateCommunity


class MainMenu(ConsoleMenu):
    """Main menu of the application."""

    def __init__(self, create_community_usecase: ICreateCommunity):
        super().__init__(
            "SIDIPP",
            "Système d'Information distribué de Dépôt d'Idées et de Prises de Position",
            exit_option_text="Quitter"
        )
        self.create_commnunity_usecase = create_community_usecase
        self.add_create_community_item()

    def _handle_create_community(self):
        """Handles the creation of a community."""
        name = self.screen.input("Nom de la communauté : ")
        description = self.screen.input("Description de la communauté : ")
        self.create_commnunity_usecase.execute(name, description)

    def add_create_community_item(self):
        """Adds an item to the menu to create a community."""
        create_community_item = FunctionItem(
            "Créer une communauté",
            self._handle_create_community
        )
        self.append_item(create_community_item)
