from sqlalchemy import create_engine, text
from flask_login import UserMixin
from app import login

engine = create_engine("db-url")


@login.user_loader
def load_user(id):

    u = UserTable()

    user = u.select_user_by_id(id)

    if len(user) > 0:
        return User(user[0])

    return None


def execute_query(query, params):

    conn = engine.connect()
    res = conn.execute(query, params)
    data = []
    try:
        data = res.fetchall()
    except Exception as e:
        pass
    finally:
        res.close()
        return data


class UserTable():

    def create_table(self):

        query = "CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY, username varchar(50), password_hash varchar(128))"

        execute_query(query, {})

    def drop_table(self):
        query = "DROP TABLE users"

        execute_query(query, {})

    def insert_user(self, params):

        query = text("INSERT INTO users (username, password_hash) VALUES (:username, :password_hash) RETURNING id")

        return execute_query(query, params)

    def select_user_by_id(self, id):
        query = text("SELECT * FROM users WHERE id = :id")
        return execute_query(query, {"id": id})

    def select_user(self, username):

        query = text("SELECT * FROM users WHERE username = :username")

        return execute_query(query, {"username": username})

    def select_username_by_id(self, id):

        return execute_query(
            text("SELECT * FROM users WHERE id = :id"),
            {"id": int(id)}
        )

    def delete_user(self, id):
        query = text("DELETE FROM users WHERE id = :id")

        return execute_query(query, {"id": id})


class User(UserMixin):

    def __init__(self, params):
        self.id = params[0]
        self.username = params[1]
        self.password_hash = params[2]


class BookTable:
    def create_table(self):

        query = "CREATE TABLE IF NOT EXISTS books (id serial PRIMARY KEY, isbn varchar(50), title varchar(150), author varchar(100)," \
                "year varchar(4))"

        execute_query(query, {})

    def truncate_table(self):

        query = "TRUNCATE TABLE books"

        execute_query(query, {})

    def drop_table(self):
        query = "DROP TABLE books"

        execute_query(query, {})

    def insert_book(self, params):

        query = text("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year) RETURNING id")

        return execute_query(query, params)

    def select_book_by_id(self, id):

        query = text("SELECT * FROM books WHERE id = :id")

        return execute_query(query, {"id": id})

    def select_book_by_isbn(self, isbn):

        query = text("SELECT * FROM books WHERE isbn = :isbn")

        return execute_query(query, {"isbn": isbn})

    def search_books(self, search_query):

        query = text("SELECT * FROM books WHERE isbn LIKE :search OR title LIKE :search OR author LIKE :search OR year LIKE :search")

        return execute_query(query, {"search": search_query})

    def delete_book(self, id):
        query = text("DELETE FROM books WHERE id = :id")

        return execute_query(query, {"id": id})


class SubmissionTable:

    def create_table(self):

        query = "CREATE TABLE IF NOT EXISTS submissions (id serial PRIMARY KEY, " \
                "submission varchar(140), rate integer, author_id integer REFERENCES users (id), " \
                "book_id integer REFERENCES books (id))"

        execute_query(query, {})

    def truncate_table(self):
        execute_query("TRUNCATE TABLE submissions", {})

    def drop_table(self):
        execute_query("DROP TABLE submissions", {})

    def insert_submission(self, params):

        query = text("INSERT INTO submissions (submission, rate, author_id, book_id) "
                     "VALUES (:submission, :rate, :author_id, :book_id) RETURNING id")

        return execute_query(query, params)

    def get_limit_submissions(self, params):

        query = text("SELECT submissions.submission AS submission, "
                     "users.username AS author, "
                     "submissions.book_id AS book_id,"
                     "submissions.rate AS rate "
                     "FROM submissions "
                     "JOIN users ON submissions.author_id = users.id "
                     "WHERE book_id = :book_id ORDER BY submissions.id DESC LIMIT :limit")

        return execute_query(query, params)

    def get_submissions_by_author_id(self, params):

        query = text("SELECT id, submission, author_id, book_id"
                     " FROM submissions WHERE author_id = :author_id AND book_id = :book_id")

        return execute_query(query, params)


class GoodreadsApi:

    __api_key = 'hsrQrzy14mUhBX8C2vpNNg'
    __api_secret = 'B9OLTHoIpH8OThYtAOsOjwkYnqluEeWC5UpryZxa7w8'
    __api_url = "https://www.goodreads.com/"

    def get_average_rating_by_isbn(self, isbn):

        import xml.etree.ElementTree as ET
        import requests

        avg_rating = "0.0"
        num_of_rates = "0"

        try:
            response = ET.fromstring(
                requests.get(self.__api_url + "search/index.html", {"key": self.__api_key, "q": str(isbn)}).text)

            avg_rating = response[1][6][0][7].text
            num_of_rates = response[1][6][0][2].text

        except Exception as e:
            pass

        finally:
            return avg_rating, num_of_rates
