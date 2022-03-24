from app.models.users import User


def test_new_user():
    user = User(
        username="user01",
        first_name="User01",
        last_name="Testing",
        email="testing01@example.com",
        password_hash=User.hash_password("TestingPassword1234"),
    )
    assert user.username == "user01"
    assert user.email == 'testing01@example.com'
    assert user.password_hash != 'TestingPassword1234'
    assert user.__repr__() == '<User user01>'
    assert user.is_authenticated
    assert user.is_active
    assert not user.is_anonymous


def test_new_user_with_fixture(new_user):
    assert new_user.username == "user01"
    assert new_user.email == 'testing01@example.com'
    assert new_user.password_hash != 'TestingPassword1234'


def test_setting_password(new_user, init_database):
    new_user.update_password('MyNewPassword')
    assert new_user.password_hash != 'MyNewPassword'
    assert new_user.verify_password('MyNewPassword')
    assert not new_user.verify_password('MyNewPassword2')
    assert not new_user.verify_password('TestingPassword1234')
