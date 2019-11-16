import sys

sys.path.append("./core")

from models import Book, Author
from database import init_db, db_session


def create_db():
    init_db()


def fill_db():
    import csv

    with open("./books.csv", newline='') as csvfile:
        book_reader = csv.reader(csvfile, delimiter=",")

        for isbn, title, author, year in book_reader:
            author = Author(author)
            db_session.add(author)

        db_session.commit()

    authors = {}

    for author in Author.query.all():
        authors[author.name] = author.id

    with open("./books.csv", newline='') as csvfile:
        book_reader = csv.reader(csvfile, delimiter=",")

        for isbn, title, author, year in book_reader:
            book = Book(isbn, title, authors[author], year)
            db_session.add(book)

        db_session.commit()


if __name__ == "__main__":

    if sys.argv[1] == "create-db":
        create_db()

    if sys.argv[1] == "fill-db":
        fill_db()
