import pytest
from application import app as application
from application import db as database

@pytest.fixture
def app():
    yield application

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db(app):
    with app.app_context():
        yield database.session

