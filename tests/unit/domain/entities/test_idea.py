from datetime import datetime

from src.domain.entities.idea import Idea
from src.domain.entities.opinion import Opinion
from src.domain.entities.member import Member


class TestIdea:
    """Test Idea class"""

    def test_init(self):
        """Validates that an idea can be created"""
        author = Member("abc", "127.0.0.1")
        idea = Idea("1", "Text", author, datetime.now())

        assert idea is not None

    def test_id_attribute(self):
        """Validates that an idea created with a specified ID has that ID"""
        id_idea = "1"
        author = Member("abc", "127.0.0.1")
        idea = Idea(id_idea, "Text", author, datetime.now())

        assert idea.identifier == id_idea

    def test_text_attribute(self):
        """Validates that an idea created with a specified text has that text"""
        text_idea = "Text"
        author = Member("abc", "127.0.0.1")
        idea = Idea("1", text_idea, author, datetime.now())

        assert idea.content == text_idea

    def test_author_attribute(self):
        """Validates that an idea created with a specified author has that author"""
        author = Member("abc", "127.0.0.1")
        idea = Idea("1", "Text", author, datetime.now())

        assert idea.author == author

    def test_creation_date_attribute(self):
        """Validates that an idea created with a specified creation date has that 
        creation date"""
        creation_date_idea = datetime.now()
        author = Member("abc", "127.0.0.1")
        idea = Idea("1", "Text", author, creation_date_idea)

        assert idea.creation_date == creation_date_idea

    def test_ideas_equality(self):
        """Validates that two ideas with the same ID are equal"""
        author = Member("abc", "127.0.0.1")
        idea = Idea("1", "Text", author, datetime.now())
        idea_copy = Idea("1", "Text", author, datetime.now())

        assert idea == idea_copy

    def test_idea_opinion_inequality(self):
        """Validates that two ideas with different IDs are not equal"""
        author = Member("abc", "127.0.0.1")
        idea = Idea("1", "Text", author, datetime.now())
        opinion = Opinion("1", "Text", author, datetime.now(), idea)

        assert idea != opinion
