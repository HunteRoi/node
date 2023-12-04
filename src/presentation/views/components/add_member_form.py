from src.domain.entities.community import Community
from src.presentation.views.generics.menu import Menu
from src.application.interfaces.iadd_member import IAddMember


class AddMemberForm:
    """Form to add a member to a community"""

    def __init__(
        self, parent_menu: Menu, community: Community, add_member_usecase: IAddMember
    ):
        self.parent_menu = parent_menu
        self.community = community
        self.add_member_usecase = add_member_usecase

    def execute(self):
        """Executes the interaction with the user"""
        ip_address = self.parent_menu.screen.input("Adresse ip du nouveau membre : ")
        port = self.parent_menu.screen.input("Port du nouveau membre : ")

        self.add_member_usecase.execute(
            self.community.identifier, ip_address, int(port)
        )
