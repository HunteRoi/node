from consolemenu.prompt_utils import UserQuit

from src.presentation.views.generics.form import Form
from src.presentation.views.generics.menu import Menu
from src.application.interfaces.icreate_community import ICreateCommunity


class CreateCommunityForm(Form):
    """Form to create a community"""

    def __init__(self, parent_menu: Menu, create_community_usecase: ICreateCommunity):
        super().__init__(parent_menu)
        self.create_community_usecase = create_community_usecase

    def execute(self):
        """Executes the interaction with the user"""
        try:
            name = self._prompt_user("Nom de la communauté", enable_quit=True)
            description = self._prompt_user(
                "Description de la communauté (Entrée pour ignorer): "
            )

            result = self.create_community_usecase.execute(name, description)

            self._print_result_message(result)
        except UserQuit:
            pass
        except:
            self._print_error("Une erreur inconnue est survenue.")
        finally:
            self._prompt_to_continue()

    def _print_result_message(self, result: str):
        """Returns the message to display to the user"""
        if result == "Success!":
            self._print_success("La communauté a été créée avec succès !")
        else:
            self._print_error(
                f"Une erreur est survenue lors de la création de la communauté :\n{result}"
            )
