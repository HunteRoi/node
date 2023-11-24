from consolemenu.items import FunctionItem, SubmenuItem

from src.presentation.views.generics.menu import Menu
from src.application.interfaces.icreate_community import ICreateCommunity
from src.application.interfaces.iadd_member import IAddMember
from src.application.interfaces.iread_communities import IReadCommunities
from src.application.interfaces.iread_ideas_from_community import IReadIdeasFromCommunity
from src.application.interfaces.iread_opinions import IReadOpinions
from src.presentation.views.components.create_community_form import (
    CreateCommunityForm
)
from src.presentation.views.menus.select_community_menu import SelectCommunityMenu


class MainMenu(Menu):
    """Main menu of the application."""

    def __init__(self,
                 create_community_usecase: ICreateCommunity,
                 add_member_usecase: IAddMember,
                 read_communities_usecase: IReadCommunities,
                 read_ideas_from_community_usecase: IReadIdeasFromCommunity,
                 read_opinions_usecase: IReadOpinions):
        super().__init__(
            "SIDIPP",
            "Système d'Information distribué de Dépôt d'Idées et de Prises de Position",
            exit_option_text="Quitter"
        )

        self.create_community_form = CreateCommunityForm(
            self,
            create_community_usecase
        )
        self.select_community_menu = SelectCommunityMenu(
            add_member_usecase,
            read_communities_usecase,
            read_ideas_from_community_usecase,
            read_opinions_usecase
        )

    def start(self, show_exit_option: bool | None = None):
        """Creates the menu and shows it"""
        self.items.clear()

        create_community_item = FunctionItem(
            "Créer une communauté",
            self.create_community_form.execute
        )
        self.append_item(create_community_item)

        read_community_item = SubmenuItem(
            "Se connecter à une communauté",
            self.select_community_menu,
            self
        )
        self.append_item(read_community_item)

        super().start(show_exit_option)
