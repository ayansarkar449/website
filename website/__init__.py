from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
db=SQLAlchemy()
DB_NAME="database.db"


def raw_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dsggfg"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .view import view
    from .auth import authe

    app.register_blueprint(view, url_prefix="/")
    app.register_blueprint(authe, url_prefix="/")
    from .models import User, Notes
    create_database(app)

    loginma = LoginManager()
    loginma.login_view = "authe.login"
    loginma.init_app(app)

    @loginma.user_loader
    def loder(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists("website/" + DB_NAME ):
        db.create_all(app=app)
        print("Created Database")

