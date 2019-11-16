from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class Book(Base):

    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    isbn = Column(String(50))
    title = Column(String(50))
    author = Column(None, ForeignKey("authors.id"))
    year = Column(String(4))

    def __init__(self, isbn=None, title=None, author=None, year=None):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year

    def to_dict(self):
        return {
            "id": self.id,
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "year": self.year
        }


class Author(Base):

    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __init__(self, name=None):
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
