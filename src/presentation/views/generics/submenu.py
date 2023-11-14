from src.presentation.views.generics.menu import Menu


class SubMenu(Menu):
    """Class to represent a submenu with a return option"""

    def __init__(self, title: str):
        super().__init__(title, exit_option_text="Retour")
