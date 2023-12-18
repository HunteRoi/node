from consolemenu.items import SubmenuItem

from src.application.interfaces.icreate_idea import ICreateIdea
from src.presentation.views.menus.community_menu import CommunityMenu
from src.presentation.views.generics.submenu import SubMenu
from src.domain.entities.community import Community
from src.application.interfaces.iadd_member import IAddMember
from src.application.interfaces.iread_communities import IReadCommunities
from src.application.interfaces.iread_ideas_from_community import (
    IReadIdeasFromCommunity,
)
from src.application.interfaces.iread_opinions import IReadOpinions
from src.application.interfaces.imachine_service import IMachineService


class SelectCommunityMenu(SubMenu):
    """The menu that displays the communities of the node."""

    def __init__(
        self,
        add_member_usecase: IAddMember,
        read_communities_usecase: IReadCommunities,
        read_ideas_from_community_usecase: IReadIdeasFromCommunity,
        read_opinions_usecase: IReadOpinions,
        create_idea_usecase: ICreateIdea,
        machine_service: IMachineService,
    ):
        super().__init__("Sélectionnez une communauté")

        self.add_member_usecase = add_member_usecase
        self.read_communities_usecase = read_communities_usecase
        self.read_ideas_from_community_usecase = read_ideas_from_community_usecase
        self.read_opinions_usecase = read_opinions_usecase
        self.create_idea_usecase = create_idea_usecase
        self.machine_service = machine_service

    def start(self, show_exit_option: bool | None = None):
        """Creates the menu with the communities and shows it"""
        self.items.clear()

        communities = self.read_communities_usecase.execute()
        for community in communities:
            self._add_community_item(community)

        super().start(show_exit_option)

    def _add_community_item(self, community: Community):
        """Adds a community item to the menu"""
        submenu = CommunityMenu(
            community,
            self.add_member_usecase,
            self.read_ideas_from_community_usecase,
            self.read_ideas_from_community_usecase,
            self.read_opinions_usecase,
            self.create_idea_usecase,
            self.machine_service,
        )
        community_item = SubmenuItem(community.name, submenu, self)
        self.append_item(community_item)
