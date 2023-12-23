from src.domain.entities.community import Community
from src.domain.entities.idea import Idea
from src.domain.entities.opinion import Opinion
from src.presentation.views.generics.menu import Menu
from src.application.interfaces.icreate_opinion import ICreateOpinion


class CreateOpinionForm:
    """Form to create an opinion into a community"""

    def __init__(
        self,
        parent_menu: Menu,
        community: Community,
        idea_or_opinion: Idea | Opinion,
        create_opinion_usecase: ICreateOpinion,
    ):
        self.parent_menu = parent_menu
        self.community = community
        self.idea_or_opinion = idea_or_opinion
        self.create_opinion_usecase = create_opinion_usecase

    def execute(self):
        """Executes the interaction with the user"""
        idea_content = self.parent_menu.screen.input("Décrivez votre opinion : ")

        self.create_opinion_usecase.execute(
            self.community.identifier, self.idea_or_opinion.identifier, idea_content
        )
