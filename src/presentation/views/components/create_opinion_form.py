from consolemenu.prompt_utils import UserQuit
from src.domain.entities.community import Community
from src.domain.entities.idea import Idea
from src.domain.entities.opinion import Opinion
from src.presentation.views.generics.form import Form
from src.presentation.views.generics.menu import Menu
from src.application.interfaces.icreate_opinion import ICreateOpinion


class CreateOpinionForm(Form):
    """Form to create an opinion into a community"""

    def __init__(
        self,
        parent_menu: Menu,
        community: Community,
        idea_or_opinion: Idea | Opinion,
        create_opinion_usecase: ICreateOpinion,
    ):
        super().__init__(parent_menu)
        self.community = community
        self.idea_or_opinion = idea_or_opinion
        self.create_opinion_usecase = create_opinion_usecase

    def execute(self):
        """Executes the interaction with the user"""
        try:
            idea_content = self._prompt_user(
                "Décrivez votre opinion : ", enable_quit=True
            )

            result = self.create_opinion_usecase.execute(
                self.community.identifier, self.idea_or_opinion.identifier, idea_content
            )

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
            self._print_success("L'opinion a été déposée avec succès!")
        else:
            self._print_error(
                f"Une erreur est survenue lors du dépôt de votre opinion :\n {result}"
            )
