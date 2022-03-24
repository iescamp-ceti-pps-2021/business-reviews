import pytest

from app import create_app, db
from app.config import app_config
from app.models.users import User


@pytest.fixture(scope="module")
def new_user():
    user = User(
        username="user01",
        first_name="User01",
        last_name="Testing",
        email="testing01@example.com",
        password_hash=User.hash_password("TestingPassword1234"),
    )
    return user


@pytest.fixture(scope="module")
def test_client():
    app = create_app(app_config["testing"])

    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope="module")
def init_database(test_client):
    db.create_all()

    user1 = User(
        username="user01",
        first_name="User01",
        last_name="Testing",
        email="testing01@example.com",
        password_hash=User.hash_password("TestingPassword1234"),
    )
    user2 = User(
        username="user02",
        first_name="User02",
        last_name="Testing",
        email="testing02@example.com",
        password_hash=User.hash_password("TestingPassword1234"),
    )
    db.session.add(user1)
    db.session.add(user2)

    db.session.commit()

    yield

    db.drop_all()


@pytest.fixture(scope="function")
def login_default_user(test_client):
    test_client.post("/auth/login", data=dict(username="user01", password="TestingPassword1234"), follow_redirects=True)

    yield

    test_client.get("/auth/logout", follow_redirects=True)
