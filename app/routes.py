from app import app
from flask import render_template, url_for, request, redirect, flash
from flask_login import current_user, login_user


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST", "GET"])
def register():

    from app.forms import RegistrationForm

    form = RegistrationForm()

    if request.method == "POST":

        if len(request.form["username"]) > 0 and len(request.form["password"]) > 0:
            from werkzeug.security import generate_password_hash
            from app.models import UserTable

            username = form.username.data
            password = form.password.data

            u = UserTable()

            res = u.select_user(username)

            if len(res) > 0:
                flash("Username busy")
                return redirect(url_for('register'))

            hash = generate_password_hash(password)

            u.insert_user({"username": username, "password_hash": hash})

            flash("Registered")
            return redirect(url_for('index'))

    return render_template("register.html", form=form, title="Registration")


@app.route("/login", methods=["POST", "GET"])
def login():

    from app.forms import LoginForm

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():

        from werkzeug.security import check_password_hash
        from app.models import UserTable, User

        username = form.username.data
        password = form.password.data

        u = UserTable()

        user_data = u.select_user(username)

        if len(user_data) <= 0:
            flash("No such user")
            return redirect(url_for('login'))

        user = User(user_data[0])

        if check_password_hash(user.password_hash, password):

            login_user(user)
            return redirect(url_for('index'))

        flash("wrong wrong wrong")
        return redirect(url_for('login'))

    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():

    from flask_login import logout_user

    logout_user()
    return redirect(url_for('index'))


@app.route("/search", methods=["POST", "GET"])
def search():

    from app.forms import SearchForm

    form = SearchForm()

    if form.validate_on_submit():

        from app.models import BookTable

        bt = BookTable()

        search_query = "%" + str(form.search.data) + "%"

        books = bt.search_books(search_query)

        return render_template("search.html", form=form, count_books=len(books), books=books, searched=True)

    return render_template("search.html", form=form, count_books=0, books=[], searched=False)


@app.route("/book/<int:id>")
def book(id):

    if int(id) <= 0:
        return redirect(url_for('index'))

    from app.forms import SubmissionsForm
    from app.models import BookTable, SubmissionTable, GoodreadsApi

    form = SubmissionsForm()

    bt = BookTable()
    st = SubmissionTable()
    gr = GoodreadsApi()

    submissions = st.get_limit_submissions({"book_id": int(id), "limit": 10})

    restrict_submissions = False

    if current_user.is_authenticated:

        if len(st.get_submissions_by_author_id({"author_id": current_user.get_id(), "book_id": int(id)})) > 0:
            restrict_submissions = True

    book = bt.select_book_by_id(int(id))

    if len(book) > 0:
        avg_rating, num_of_rates = gr.get_average_rating_by_isbn(str(book[0][1]))

        return render_template("book.html", book=book[0], form=form, submissions=submissions,
                               restrict_submissions=restrict_submissions, avg_rating=avg_rating, num_of_rates=num_of_rates)

    return redirect(url_for('index'))


@app.route("/post_submission", methods=["POST"])
def post_submission():

    from app.forms import SubmissionsForm
    from app.models import SubmissionTable

    form = SubmissionsForm()

    if form.validate_on_submit():
        st = SubmissionTable()

        st.insert_submission({"submission": form.submission.data,
                                "rate": form.rate.data,
                                "author_id": current_user.get_id(),
                                "book_id": int(form.book_id.data)})

    return redirect(url_for('book', id=int(form.book_id.data)))


@app.route("/post_rate")
def post_rate():
    pass


@app.route("/api/1.0/<string:isbn>")
def api(isbn):

    import json

    response = {"error": "book not found"}

    if len(isbn) > 0:

        from app.models import BookTable

        bt = BookTable()

        res = bt.select_book_by_isbn(isbn)

        if len(res) > 0:
            response = {}

            keys_dict = {"0": "id", "1": "isbn", "2": "title", "3": "author", "4": "year"}

            for key, value in enumerate(res[0]):
                response[keys_dict[str(key)]] = value

    return render_template("api.html", response=json.dumps(response))
