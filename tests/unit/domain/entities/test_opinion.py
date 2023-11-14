from datetime import datetime

from src.domain.entities.opinion import Opinion
from src.domain.entities.member import Member
from src.domain.entities.idea import Idea


class TestOpinion:
    """Test opinion class"""

    def test_init(self):
        """Validates that an opinion can be created"""
        author = Member("abc", "127.0.0.1")
        idea = Idea("1", "Text", author, datetime.now())

        opinion = Opinion("1", "Text", author, datetime.now(), idea)

        assert opinion is not None

    def test_id_attribute(self):
        """Validates that an opinion created with a specified ID has that ID"""
        id_opinion = "1"
        author = Member("abc", "127.0.0.1")
        idea = Idea("1", "Text", author, datetime.now())
        opinion = Opinion(id_opinion, "Text", author, datetime.now(), idea)

        assert opinion.identifier == id_opinion

    def test_text_attribute(self):
        """Validates that an opinion created with a specified text has that text"""
        text_opinion = "Text"
        author = Member("abc", "127.0.0.1")
        idea = Idea("1", "Text", author, datetime.now())
        opinion = Opinion("1", text_opinion, author, datetime.now(), idea)

        assert opinion.content == text_opinion

    def test_author_attribute(self):
        """Validates that an opinion created with a specified author has that author"""
        author = Member("abc", "127.0.0.1")
        idea = Idea("1", "Text", author, datetime.now())
        opinion = Opinion("1", "Text", author, datetime.now(), idea)

        assert opinion.author == author

    def test_creation_date_attribute(self):
        """Validates that an opinion created with a specified creation date has 
        that creation date"""

        creation_date_opinion = datetime.now()
        author = Member("abc", "127.0.0.1")
        idea = Idea("1", "Text", author, datetime.now())
        opinion = Opinion("1", "Text", author, creation_date_opinion, idea)

        assert opinion.creation_date == creation_date_opinion

    def test_message_parent_attribute(self):
        """Validates that an opinion created with a specified message parent 
        has that message parent"""

        author = Member("abc", "127.0.0.1")
        idea = Idea("1", "Text", author, datetime.now())
        opinion = Opinion("1", "Text", author, datetime.now(), idea)

        assert opinion.parent == idea

    def test_on_opinion(self):
        """Validates that an opinion created with a specified message parent has 
        that message parent on opinion"""

        author = Member("abc", "127.0.0.1")
        idea = Idea("1", "Text", author, datetime.now())
        parent_opinion = Opinion("1", "Text", author, datetime.now(), idea)
        opinion = Opinion("2", "Text", author, datetime.now(), parent_opinion)

        assert opinion.parent == parent_opinion
        assert opinion.parent.parent == idea

    def test_opinions_equality(self):
        """Validates that two ideas with the same ID are equal"""
        author = Member("abc", "127.0.0.1")
        idea = Idea("1", "Text", author, datetime.now())
        opinion = Opinion("2", "Text", author, datetime.now(), idea)
        opinion_copy = Opinion("2", "Text", author, datetime.now(), idea)

        assert opinion == opinion_copy

    def test_opinion_idea_inequality(self):
        """Validates that two ideas with different IDs are not equal"""
        author = Member("abc", "127.0.0.1")
        idea = Idea("1", "Text", author, datetime.now())
        opinion = Opinion("1", "Text", author, datetime.now(), idea)

        assert opinion != idea
