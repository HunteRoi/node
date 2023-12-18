from src.presentation.views.generics.menu import Menu
from src.application.interfaces.icreate_community import ICreateCommunity


class CreateCommunityForm:
    """Form to create a community"""

    def __init__(self, parent_menu: Menu, create_community_usecase: ICreateCommunity):
        self.parent_menu = parent_menu
        self.create_community_usecase = create_community_usecase

    def execute(self):
        """Executes the interaction with the user"""
        name = self.parent_menu.screen.input("Nom de la communauté : ")
        description = self.parent_menu.screen.input(
            "Description de la communauté (Entrée pour ignorer): "
        )
        self.create_community_usecase.execute(name, description)
