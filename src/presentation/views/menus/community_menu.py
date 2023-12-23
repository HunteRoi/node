from consolemenu.items import SubmenuItem, FunctionItem

from src.application.interfaces.icreate_idea import ICreateIdea
from src.application.interfaces.icreate_opinion import ICreateOpinion
from src.presentation.views.components.create_idea_form import CreateIdeaForm
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
from src.application.interfaces.imachine_service import IMachineService


class CommunityMenu(SubMenu):
    """The menu that displays the actions that can be done on a community."""

    def __init__(
        self,
        community: Community,
        add_member_usecase: IAddMember,
        read_communities_usecase: IReadCommunities,
        read_ideas_from_community_usecase: IReadIdeasFromCommunity,
        read_opinions_usecase: IReadOpinions,
        create_idea_usecase: ICreateIdea,
        create_opinion_usecase: ICreateOpinion,
        machine_service: IMachineService,
    ):
        super().__init__(f'Communauté "{community.name}"')

        self.community = community
        self.add_member_usecase = add_member_usecase
        self.read_communities_usecase = read_communities_usecase
        self.read_ideas_from_community_usecase = read_ideas_from_community_usecase
        self.read_opinions_usecase = read_opinions_usecase
        self.create_idea_usecase = create_idea_usecase
        self.create_opinion_usecase = create_opinion_usecase
        self.machine_service = machine_service

        self.add_member_item = FunctionItem(
            "Ajouter un membre",
            AddMemberForm(
                self, self.community, self.add_member_usecase, self.machine_service
            ).execute,
        )
        self.create_idea_item = FunctionItem(
            "Poster une idée",
            CreateIdeaForm(self, self.community, self.create_idea_usecase).execute,
        )
        self.community_item = SubmenuItem(
            "Lire les idées de la communauté",
            ReadIdeasMenu(
                self.community,
                self.read_ideas_from_community_usecase,
                self.read_opinions_usecase,
                self.create_opinion_usecase,
            ),
            self,
        )

    def draw(self):
        """Creates the menu with the communities and shows it"""
        if self.add_member_item not in self.items:
            self.append_item(self.add_member_item)
        if self.create_idea_item not in self.items:
            self.append_item(self.create_idea_item)
        if self.community_item not in self.items:
            self.append_item(self.community_item)
        super().draw()
