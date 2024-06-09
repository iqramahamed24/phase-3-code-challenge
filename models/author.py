class Author:
    def __init__(self, id, name):
        self._id = id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if hasattr(self, '_name'):
            raise AttributeError("Name cannot be changed after instantiation.")
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        if len(value) == 0:
            raise ValueError("Name must not be empty.")
        self._name = value

    def create_author(self, cursor):
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (self._name,))
        self._id = cursor.lastrowid

    @classmethod
    def get_all_authors(cls, cursor):
        cursor.execute("SELECT id, name FROM authors")
        authors_data = cursor.fetchall()
        return [cls(id=row[0], name=row[1]) for row in authors_data]

    def magazines(self, cursor):
        cursor.execute("""
            SELECT magazines.*
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """, (self._id,))
        return cursor.fetchall()

    def articles(self, cursor):
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self._id,))
        return cursor.fetchall()
