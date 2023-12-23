from consolemenu.items import FunctionItem, SubmenuItem
from src.application.interfaces.icreate_opinion import ICreateOpinion
from src.presentation.views.components.create_opinion_form import CreateOpinionForm

from src.presentation.views.generics.submenu import SubMenu
from src.domain.entities.community import Community
from src.domain.entities.idea import Idea
from src.domain.entities.opinion import Opinion
from src.application.interfaces.iread_opinions import IReadOpinions


class ReadOpinionsMenu(SubMenu):
    """The menu that displays the opinions of an idea or an opinion."""

    def __init__(
        self,
        community: Community,
        parent_: Idea | Opinion,
        read_opinions_usecase: IReadOpinions,
        create_opinion_usecase: ICreateOpinion,
    ):
        super().__init__(self._get_menu_title(parent_))

        # self.parent is inherited from ConsoleMenu which means
        # it cannot be used as a custom class attribute
        # so it's named parent_
        self.parent_ = parent_
        self.community = community
        self.read_opinions_usecase = read_opinions_usecase
        self.create_opinion_usecase = create_opinion_usecase
        self.create_opinion_form = CreateOpinionForm(
            self, self.community, self.parent_, self.create_opinion_usecase
        )

    def _get_menu_title(self, parent_: Idea | Opinion) -> str:
        """Builds the menu title"""
        title = "l'idée" if isinstance(parent_, Idea) else "la prise de position"
        name = '"' + parent_.content + '"'
        return f"Les prises de position de {title} {name}"

    def draw(self):
        """Creates the menu with the opinions and shows it"""
        self.items.clear()

        self._add_form_item()
        opinions = self.read_opinions_usecase.execute(
            self.community.identifier, self.parent_.identifier
        )
        for opinion in opinions:
            self._add_opinion_item(opinion)
        self.add_exit()

        super().draw()

    def _add_form_item(self):
        """Adds an item to create an opinion"""
        create_opinion_item = FunctionItem(
            "Poster une prise de position", self.create_opinion_form.execute
        )
        self.append_item(create_opinion_item)

    def _add_opinion_item(self, opinion: Opinion):
        """Adds an opinion item to the menu"""
        submenu = ReadOpinionsMenu(
            self.community,
            opinion,
            self.read_opinions_usecase,
            self.create_opinion_usecase,
        )
        item = SubmenuItem(opinion.content, submenu, self)
        self.append_item(item)
