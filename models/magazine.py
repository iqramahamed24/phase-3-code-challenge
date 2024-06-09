class Magazine:
    def __init__(self, id, name, category):
        self._id = id
        self.name = name
        self.category = category

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._validate_name(value)
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._validate_category(value)
        self._category = value

    @staticmethod
    def _validate_name(name):
        if not (isinstance(name, str) and 2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")

    @staticmethod
    def _validate_category(category):
        if not (isinstance(category, str) and category):
            raise ValueError("Category must be a non-empty string")

    def save(self, cursor):
        if self._id is None:
            cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self._name, self._category))
            self._id = cursor.lastrowid
        else:
            cursor.execute("UPDATE magazines SET name = ?, category = ? WHERE id = ?", 
                           (self._name, self._category, self._id))

    @classmethod
    def fetch_all(cls, cursor):
        cursor.execute("SELECT id, name, category FROM magazines")
        return [cls(id, name, category) for id, name, category in cursor.fetchall()]

    def fetch_articles(self, cursor):
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self._id,))
        return cursor.fetchall()

    def fetch_contributors(self, cursor):
        cursor.execute("""
            SELECT authors.*
            FROM authors
            INNER JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """, (self._id,))
        return cursor.fetchall()

    def fetch_article_titles(self, cursor):
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self._id,))
        return [row[0] for row in cursor.fetchall()] or None

    def fetch_contributing_authors(self, cursor):
        cursor.execute("""
            SELECT authors.*, COUNT(articles.id) AS article_count
            FROM authors
            INNER JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        """, (self._id,))
        return cursor.fetchall() or None
