import unittest
from unittest.mock import MagicMock
from models.author import Author
from models.article import Article
from models.magazine import Magazine

class TestModels(unittest.TestCase):
    def setUp(self):
        self.cursor = MagicMock()

    def test_create_author(self):
        author = Author(None, "John Doe")
        author.create_author(self.cursor)
        self.cursor.execute.assert_called_once_with("INSERT INTO authors (name) VALUES (?)", ("John Doe",))

    def test_article_creation(self):
        article = Article(1, "Test Title", "Test Content", 1, 1)
        self.assertEqual(article.title, "Test Title")

    def test_author_creation(self):
        author = Author(1, "John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_magazine_creation(self):
        magazine = Magazine(1, "Tech Weekly", "Technology")
        self.assertEqual(magazine.name, "Tech Weekly")

    def test_get_all_authors(self):
        self.cursor.fetchall.return_value = [(1, "John Doe"), (2, "John Doe")]
        authors = Author.get_all_authors(self.cursor)
        self.cursor.execute.assert_called_once_with("SELECT id, name FROM authors")
        self.assertEqual(len(authors), 2)
        self.assertEqual(authors[0].id, 1)
        self.assertEqual(authors[0].name, "John Doe")
        self.assertEqual(authors[1].id, 2)
        self.assertEqual(authors[1].name, "John Doe")



if __name__ == "__main__":
    unittest.main()
