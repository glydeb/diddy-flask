import os
from flask import Flask
from .extensions import api, db, jwt
from .api_namespace import ns
from .models import User
from dotenv import load_dotenv

def create_app(database_uri="sqlite:///db.sqlite3"):
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config['RESTX_ERROR_404_HELP'] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    db.init_app(app)
    jwt.init_app(app)

    api.init_app(app)
    api.add_namespace(ns)


    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        query = db.select(User).where(User.id == identity)
        user = db.execute(query)
        return db.execute(query)

    return app