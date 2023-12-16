from src.domain.entities.community import Community
from src.presentation.views.generics.menu import Menu
from src.application.interfaces.icreate_idea import ICreateIdea


class CreateIdeaForm:
    """Form to create an idea into a community"""

    def __init__(
        self, parent_menu: Menu, community: Community, create_idea_usecase: ICreateIdea
    ):
        self.parent_menu = parent_menu
        self.community = community
        self.create_idea_usecase = create_idea_usecase

    def execute(self):
        """Executes the interaction with the user"""
        idea_content = self.parent_menu.screen.input("Décrivez votre idée : ")

        self.create_idea_usecase.execute(self.community.identifier, idea_content)
