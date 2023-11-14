from consolemenu.items import SubmenuItem

from src.presentation.views.menus.read_ideas_menu import ReadIdeasMenu
from src.presentation.views.generics.submenu import SubMenu
from src.domain.entities.community import Community
from src.application.interfaces.iread_communities import IReadCommunities
from src.application.interfaces.iread_ideas_from_community import IReadIdeasFromCommunity
from src.application.interfaces.iread_opinions import IReadOpinions


class SelectCommunityMenu(SubMenu):
    """The menu that displays the communities of the node."""

    def __init__(self,
                 read_communities_usecase: IReadCommunities,
                 read_ideas_from_community_usecase: IReadIdeasFromCommunity,
                 read_opinions_usecase: IReadOpinions):
        super().__init__("Sélectionnez une communauté")

        self.read_communities_usecase = read_communities_usecase
        self.read_ideas_from_community_usecase = read_ideas_from_community_usecase
        self.read_opinions_usecase = read_opinions_usecase

    def start(self, show_exit_option: bool | None = None):
        """Creates the menu with the communities and shows it"""
        self.items.clear()

        communities = self.read_communities_usecase.execute()
        for community in communities:
            submenu = ReadIdeasMenu(
                community,
                self.read_ideas_from_community_usecase,
                self.read_opinions_usecase
            )
            self._add_community_item(community, submenu)

        return super().start(show_exit_option)

    def _add_community_item(self, community: Community, submenu: SubMenu):
        """Adds a community item to the menu"""
        community_item = SubmenuItem(
            community.name,
            submenu,
            self
        )
        self.append_item(community_item)
