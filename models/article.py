class Article:
    def __init__(self, id, title, content, author, magazine):
        self._id = id
        self.title = title
        self.content = content
        self._author = author
        self._magazine = magazine

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._validate_title(value)
        self._title = value

    @staticmethod
    def _validate_title(value):
        if not isinstance(value, str) or not (5 <= len(value) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters.")

    def save(self, cursor):
        if self._id is None:
            cursor.execute("INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)", 
                           (self._title, self.content, self._author, self._magazine))
            self._id = cursor.lastrowid
        else:
            cursor.execute("UPDATE articles SET title = ?, content = ?, author_id = ?, magazine_id = ? WHERE id = ?", 
                           (self._title, self.content, self._author, self._magazine, self._id))

    @classmethod
    def fetch_all_titles(cls, cursor):
        cursor.execute("SELECT title FROM articles")
        titles = cursor.fetchall()
        return [title[0] for title in titles] if titles else None

    def fetch_magazine_name(self, cursor):
        cursor.execute("SELECT name FROM magazines WHERE id = ?", (self._magazine,))
        magazine_name = cursor.fetchone()
        return magazine_name[0] if magazine_name else None

    def fetch_author_name(self, cursor):
        cursor.execute("SELECT name FROM authors WHERE id = ?", (self._author,))
        author_name = cursor.fetchone()
        return author_name[0] if author_name else None

    @classmethod
    def create(cls, cursor, title, content, author_id, magazine_id):
        cursor.execute("INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)", 
                       (title, content, author_id, magazine_id))
        article_id = cursor.lastrowid
        return cls(article_id, title, content, author_id, magazine_id)
