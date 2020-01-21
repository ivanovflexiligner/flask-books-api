from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = b'secret'
login = LoginManager(app)

from app import routes, models
