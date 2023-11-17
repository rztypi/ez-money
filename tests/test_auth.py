from flask import g, session

from ezmoney.db import get_db
from ezmoney.auth import save_user


def test_login(client, auth):
    assert client.get("/auth/login").status_code == 302

    auth.login_session()
    with client:
        client.get("/")
        assert "user_id" in session
        assert g.user["email"] == "hello_world@gmail.com"


def test_logout(client, auth):
    auth.login_session()
    with client:
        client.get("/auth/logout")
        assert "user_id" not in session


def test_save_user(app):
    userinfo = {
        "sub": "thisisatestid",
        "email": "hello_word@gmail.com",
        "given_name": "Hello",
        "family_name": "World",
    }
    with app.app_context():
        save_user(userinfo)
        assert len(get_db().execute("SELECT * FROM user").fetchall()) == 2

        userinfo["sub"] = "adifferenttestid"
        save_user(userinfo)
        assert len(get_db().execute("SELECT * FROM user").fetchall()) == 3
