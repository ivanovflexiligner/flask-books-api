from flask import Flask, jsonify, make_response
import sys

sys.path.append("./core")

from models import Book, Author
from database import db_session

app = Flask(__name__)


@app.route("/books/api/1.0/books")
def get_all_books():

    to_json_books = []

    for book in Book.query.all():
        to_json_books.append(
            book.to_dict()
        )

    return jsonify(to_json_books)


@app.route("/books/api/1.0/books/<int:isbn>", methods=["GET"])
def get_book_by_isbn(isbn):

    try:
        book = db_session.query(Book).filter(Book.isbn == isbn)[0]
    except Exception as e:
        return make_response(jsonify({"error": "Not Found"}), 404)

    return jsonify(book.to_dict())

