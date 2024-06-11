from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author



    
def create_author(cursor):
    author_name = input("Enter author name: ")
    author = Author(None, author_name)
    author.create_author(cursor)
    print("Author created Successfully")

def get_all_authors(cursor):
    authors = Author.get_all_authors(cursor)
    if authors:
        print("All Author:")
        for author in authors:
            print(f"ID: {author.id}, Name: {author.name}")
    else:
        print("No author found.")

def get_author_articles(cursor):
    author_id = input("Enter the author ID to display articles: ")
    author = Author(author_id, None)
    articles = author.articles(cursor)
    if articles:
        print(f"Articles associated with Author ID {author_id}:")
        for article in articles:
            print(f"ID: {article[0]}, Title: {article[1]}, Content: {article[2]}")
    else:
        print(f"No articles found for Author ID {author_id}.")

def get_author_magazines(cursor):
    author_id = input("Enter the author ID to display magazines: ")
    author = Author(author_id, None)
    magazines = author.magazines(cursor)
    if magazines:
        print(f"Magazines associated with Author ID {author_id}:")
        for magazine in magazines:
            print(f"ID: {magazine[0]}, Name: {magazine[1]}")
    else:
        print(f"No magazines found for Author ID {author_id}.")



     
def create_article(cursor):
    title = input("Enter article title: ")
    content = input("Enter article content: ")
    author_id = input("Enter author ID: ")
    magazine_id = input("Enter magazine ID: ")
    Article.create_article(cursor, title, content, author_id, magazine_id)
    print("Article created successfully.")

def get_article_title(cursor):
    conn = get_db_connection()
    cursor = conn.cursor()
    titles = Article.get_title(cursor)
    if titles:
        print("Article Titles:")
        for title in titles:
           print(f"Title '{title}'")
    else:
        print("No articles found.")

def get_article_author(cursor):
    article_id = input("Enter the article ID to display the author: ")
    cursor.execute("SELECT title, content, author_id, magazine_id FROM articles WHERE id = ?", (article_id,))
    article_details = cursor.fetchone()

    if article_details:
        title, content, author_id, magazine_id = article_details
        article = Article(article_id, title, content, author_id, magazine_id)
        author = article.get_author(cursor)
        if author:
            print(f"Author of Article ID {article_id}: , Authors Name :{author}")
        else:
            print(f"No author found for Article ID {article_id}.")
    else:
        print(f"No article found with ID {article_id}.")

def create_magazine(cursor):
    name = input("Enter magazine name: ")
    category = input("Enter magazine category: ")
    cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (name, category))
    print("Magazine created successfully.")

def get_magazine(cursor):
    article_id = input("Enter the article ID to display the magazine: ")
    cursor.execute("SELECT title, content, author_id, magazine_id FROM articles WHERE id = ?", (article_id,))
    article_details = cursor.fetchone()

    if article_details:
        title, content, author_id, magazine_id = article_details
        article = Article(article_id, title, content, author_id, magazine_id)
        magazine = article.get_magazine(cursor)
        if magazine:
            print(f"Magazine of Article ID {article_id}: , Magazine Name {magazine}")
        else:
            print(f"No magazine found for Article ID {article_id}.")
    else:
        print(f"No article found with ID {article_id}.")




def main():
    create_tables()


    while True:
        print("\nChoose:")
        print("1.  Create Author")
        print("2.  Create Magazine")
        print("3.  Create Article")
        choice = input("Enter A Number: ")

        if choice == "1":
            conn = get_db_connection()
            cursor = conn.cursor()
            create_author(cursor)
            conn.commit()
            conn.close()
        elif choice == "2":
            conn = get_db_connection()
            cursor = conn.cursor()
            create_magazine(cursor)
            conn.commit()
            conn.close()
        elif choice == "3":
            conn = get_db_connection()
            cursor = conn.cursor()
            create_article(cursor)
            conn.commit()
            conn.close()
        else:
            print("Invalid option. Please enter a valid option.")


if __name__ == "__main__":
    main()