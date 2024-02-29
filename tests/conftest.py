import pytest
from app import create_app, db
from app.models import User

@pytest.fixture()
def app():
    app = create_app("sqlite://")
    with app.app_context():
        db.create_all()

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
