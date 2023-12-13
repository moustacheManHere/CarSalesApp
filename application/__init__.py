from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile("config.cfg")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()
login_manager = LoginManager()

with app.app_context():
    login_manager.init_app(app)
    db.init_app(app)

    from .models import *

    db.create_all()
    populate_cars()
    db.session.commit()
    print("Created Database!")

from application import routes
