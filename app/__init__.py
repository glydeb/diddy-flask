from flask import Flask
from .extensions import api, db
from .api_namespace import ns

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

    db.init_app(app)

    api.init_app(app)
    api.add_namespace(ns)

    return app