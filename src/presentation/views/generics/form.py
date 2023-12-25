from consolemenu import PromptUtils

from src.presentation.views.color_utils import Color, to_color, Format
from src.presentation.views.generics.menu import Menu


class Form:
    """A form is a screen that allows the user to enter some data"""

    def __init__(self, parent_menu: Menu):
        self.parent_menu = parent_menu

    def _print_error(self, message: str):
        """Prints an error message to the user"""
        self.parent_menu.screen.println(f"{to_color(message, Color.RED_FOREGROUND)}")

    def _print_success(self, message: str):
        """Prints a success message to the user"""
        self.parent_menu.screen.println(f"{to_color(message, Color.GREEN_FOREGROUND)}")

    def _prompt_user(self, message: str, enable_quit: bool = False) -> str:
        """Prompts the user for a string"""
        return (
            PromptUtils(self.parent_menu.screen)
            .input(
                message,
                enable_quit=enable_quit,
                quit_message="(q pour quitter)",
            )
            .input_string
        )

    def _prompt_to_continue(self):
        """Prompts the user to continue"""
        PromptUtils(self.parent_menu.screen).enter_to_continue(
            f"Appuyez sur {to_color('entrée', text_format=Format.BOLD)} pour continuer."
        )
