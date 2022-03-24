def test_login_page(test_client):
    response = test_client.get("/auth/login")
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Username" in response.data
    assert b"Password" in response.data


def test_valid_login_logout(test_client, init_database):
    response = test_client.post(
        "/auth/login", data=dict(username="user01", password="TestingPassword1234"), follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Hola!" in response.data
    assert b"user01" in response.data
    assert b"Log Out" in response.data
    assert b"Sign In" not in response.data
    assert b"Sign Up" not in response.data

    response = test_client.get("/auth//logout", follow_redirects=True)
    assert b"Hola!" not in response.data
    assert b"user01" not in response.data
    assert b"Log Out" not in response.data
    assert b"Sign In" in response.data
    assert b"Sign Up" in response.data


def test_invalid_login(test_client, init_database):
    pass


def test_login_already_logged_in(test_client, init_database, login_default_user):
    pass


def test_valid_registration(test_client, init_database):
    pass


def test_invalid_registration(test_client, init_database):
    pass


def test_duplicate_registration(test_client, init_database):
    pass
