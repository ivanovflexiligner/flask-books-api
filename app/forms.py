from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, HiddenField, SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


class SearchForm(FlaskForm):
    search = StringField("search", validators=[DataRequired()])


class SubmissionsForm(FlaskForm):
    submission = TextAreaField("submission", validators=[DataRequired()])
    rate = SelectField("rate", choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])
    book_id = HiddenField("book_id")
