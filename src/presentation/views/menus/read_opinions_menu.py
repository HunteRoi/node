from consolemenu.items import SubmenuItem

from src.presentation.views.generics.submenu import SubMenu
from src.domain.entities.community import Community
from src.domain.entities.idea import Idea
from src.domain.entities.opinion import Opinion
from src.application.interfaces.iread_ideas_from_community import IReadIdeasFromCommunity
from src.application.interfaces.iread_opinions import IReadOpinions


class ReadOpinionsMenu(SubMenu):
    """The menu that displays the opinions of an idea or an opinion."""

    def __init__(self,
                 community: Community,
                 parent: Idea | Opinion,
                 read_ideas_usecase: IReadIdeasFromCommunity,
                 read_opinions_usecase: IReadOpinions):
        super().__init__(self._get_menu_title(parent))

        self.parent = parent
        self.community = community
        self.read_ideas_usecase = read_ideas_usecase
        self.read_opinions_usecase = read_opinions_usecase

    def _get_menu_title(self, parent: Idea | Opinion) -> str:
        """Builds the menu title"""
        if isinstance(parent, Idea):
            return f"Les prises de position de l'idée \"{parent.content}\""
        else:
            return f"Les prises de position de la prise de position \"{parent.content}\""

    def start(self, show_exit_option: bool | None = None):
        """Creates the menu with the opinions and shows it"""
        self.items.clear()

        opinions = self.read_opinions_usecase.execute(
            self.community.identifier,
            self.parent.identifier
        )
        for opinion in opinions:
            self._add_opinion_item(opinion)

        return super().start(show_exit_option)

    def _add_opinion_item(self, opinion: Opinion):
        """Adds an opinion item to the menu"""
        submenu = ReadOpinionsMenu(self.community,
                                   opinion,
                                   self.read_ideas_usecase,
                                   self.read_opinions_usecase)
        item = SubmenuItem(
            opinion.content,
            submenu,
            self
        )
        self.append_item(item)
