import pytest
from app import create_app, db

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def test_user(app):
    user = db.User(name='John Doe', email='johndoe@example.com')
    db.session.add(user)
    db.session.commit()
    return user