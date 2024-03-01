from flask import Flask
from .extensions import api, db
from .api_namespace import ns

def create_app(database_uri="sqlite:///db.sqlite3"):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config['RESTX_ERROR_404_HELP'] = False

    db.init_app(app)

    api.init_app(app)
    api.add_namespace(ns)

    return app