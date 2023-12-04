from consolemenu.items import SubmenuItem, FunctionItem

from src.presentation.views.menus.read_ideas_menu import ReadIdeasMenu
from src.presentation.views.components.add_member_form import AddMemberForm
from src.presentation.views.generics.submenu import SubMenu
from src.domain.entities.community import Community
from src.application.interfaces.iadd_member import IAddMember
from src.application.interfaces.iread_communities import IReadCommunities
from src.application.interfaces.iread_ideas_from_community import (
    IReadIdeasFromCommunity,
)
from src.application.interfaces.iread_opinions import IReadOpinions


class CommunityMenu(SubMenu):
    """The menu that displays the actions that can be done on a community."""

    def __init__(
        self,
        community: Community,
        add_member_usecase: IAddMember,
        read_communities_usecase: IReadCommunities,
        read_ideas_from_community_usecase: IReadIdeasFromCommunity,
        read_opinions_usecase: IReadOpinions,
    ):
        super().__init__(f'Communauté "{community.name}"')

        self.community = community
        self.add_member_usecase = add_member_usecase
        self.read_communities_usecase = read_communities_usecase
        self.read_ideas_from_community_usecase = read_ideas_from_community_usecase
        self.read_opinions_usecase = read_opinions_usecase

        self.add_member_form = AddMemberForm(
            self, self.community, self.add_member_usecase
        )

    def start(self, show_exit_option: bool | None = None):
        """Creates the menu with the communities and shows it"""
        self.items.clear()

        add_member_item = FunctionItem(
            "Ajouter un membre", self.add_member_form.execute
        )
        self.append_item(add_member_item)

        submenu = ReadIdeasMenu(
            self.community,
            self.read_ideas_from_community_usecase,
            self.read_opinions_usecase,
        )
        community_item = SubmenuItem("Lire les idées de la communauté", submenu, self)
        self.append_item(community_item)

        super().start(show_exit_option)
