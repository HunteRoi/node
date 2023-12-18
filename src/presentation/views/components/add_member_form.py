from src.domain.entities.community import Community
from src.presentation.views.generics.menu import Menu
from src.application.interfaces.iadd_member import IAddMember
from src.application.interfaces.imachine_service import IMachineService


class AddMemberForm:
    """Form to add a member to a community"""

    def __init__(
        self,
        parent_menu: Menu,
        community: Community,
        add_member_usecase: IAddMember,
        machine_service: IMachineService,
    ):
        self.parent_menu = parent_menu
        self.community = community
        self.add_member_usecase = add_member_usecase
        self.machine_service = machine_service

    def execute(self):
        """Executes the interaction with the user"""
        ip_address = self.parent_menu.screen.input("Adresse ip du nouveau membre : ")

        self.add_member_usecase.execute(
            self.community.identifier, ip_address, self.machine_service.get_port()
        )
