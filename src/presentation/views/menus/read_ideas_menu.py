from consolemenu.items import SubmenuItem
from src.application.interfaces.icreate_opinion import ICreateOpinion

from src.application.interfaces.iread_ideas_from_community import (
    IReadIdeasFromCommunity,
)
from src.application.interfaces.iread_opinions import IReadOpinions
from src.presentation.views.menus.read_opinions_menu import ReadOpinionsMenu
from src.presentation.views.generics.submenu import SubMenu
from src.domain.entities.community import Community
from src.domain.entities.idea import Idea


class ReadIdeasMenu(SubMenu):
    """The menu that displays the ideas of a community."""

    def __init__(
        self,
        community: Community,
        read_ideas_usecase: IReadIdeasFromCommunity,
        read_opinions_usecase: IReadOpinions,
        create_opinion_usecase: ICreateOpinion,
    ):
        super().__init__(f'Les idées de la communauté "{community.name}"')

        self.community = community
        self.read_ideas_usecase = read_ideas_usecase
        self.read_opinions_usecase = read_opinions_usecase
        self.create_opinion_usecase = create_opinion_usecase

    def draw(self):
        """Creates the menu with the ideas and shows it"""
        self.items.clear()

        ideas = self.read_ideas_usecase.execute(self.community.identifier)
        for idea in ideas:
            self._add_idea_item(idea)
        self.add_exit()

        super().draw()

    def _add_idea_item(self, idea: Idea):
        """Adds an idea item to the menu"""
        submenu = ReadOpinionsMenu(
            self.community,
            idea,
            self.read_opinions_usecase,
            self.create_opinion_usecase,
        )
        item = SubmenuItem(idea.content, submenu, self)
        self.append_item(item)
