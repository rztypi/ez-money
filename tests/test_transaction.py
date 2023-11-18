from datetime import date

import pytest

from ezmoney.db import get_db


def test_index(client, auth):
    response = client.get("/")
    assert b"An EZ money tracker." in response.data
    assert b"Log In" in response.data

    auth.login_session()
    response = client.get("/")
    assert b"Balance:" in response.data
    assert b"Add Transaction" in response.data
    assert b"Log Out" in response.data
    assert b"this is an expense" in response.data
    assert b"this is an income" in response.data
    assert "₱1,000.00".encode() in response.data
    assert f"{date.today()}".encode() in response.data
    assert b"barGraph" in response.data

    response = client.get("/", query_string={"t": "week"})
    assert b"labels: [7, 6, 5, 4, 3, 2, 1, 0]" in response.data

    response = client.get("/", query_string={"t": "month"})
    assert b"labels: [30, 29, 28, " in response.data
    
    response = client.get("/", query_string={"t": "year"})
    assert b"labels: [365, 364, 363, " in response.data

    response = client.get("/", query_string={"t": "gibberish"})
    assert b"labels: [0]" in response.data

    auth.logout()
    auth.login_session(user_id="notransactions")
    response = client.get("/")
    print(response.data)
    assert b"No transactions" in response.data


@pytest.mark.parametrize("path", (
    "/add",
    "/edit/1",
    "/delete/1",
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_edit(app, client, auth):
    auth.login_session()
    data = {
        "amount": -1000,
        "description": "this has been updated",
        "date": date.today(),
    }
    response = client.post("/edit/999", data=data, follow_redirects=True)
    assert b"Transaction does not exist." in response.data

    response = client.post("/edit/1", data=data)
    with app.app_context():
        transaction = get_db().execute("SELECT * FROM transactions WHERE id = 1").fetchone()
        assert transaction["description"] == "this has been updated"


@pytest.mark.parametrize(("path", "message"), (
    ("/add", b"Transaction added."),
    ("/edit/1", b"Transaction updated."),
))
def test_add_edit_validate(client, auth, path, message):
    auth.login_session()
    data = {
        "amount": None,
        "description": None,
        "date": None,
    }
    response = client.post(path, data=data, follow_redirects=True)
    assert b"Amount must be provided." in response.data

    data["amount"] = "an invalid amount"
    response = client.post(path, data=data, follow_redirects=True)
    assert b"Description must be provided." in response.data

    data["description"] = "     "
    response = client.post(path, data=data, follow_redirects=True)
    assert b"Date must be provided." in response.data

    data["date"] = "9999-99-99"
    response = client.post(path, data=data, follow_redirects=True)
    assert b"Invalid amount." in response.data

    data["amount"] = 1000
    response = client.post(path, data=data, follow_redirects=True)
    assert b"Invalid description." in response.data

    data["description"] = "a proper description"
    response = client.post(path, data=data, follow_redirects=True)
    assert b"Invalid date." in response.data

    data["date"] = "2012-12-12"
    response = client.post(path, data=data, follow_redirects=True)
    assert message in response.data


def test_delete(app, client, auth):
    auth.login_session()
    response = client.post("/delete/999", follow_redirects=True)
    assert b"Transaction cannot be deleted." in response.data

    response = client.post("/delete/1", follow_redirects=True)
    assert b"Transaction deleted." in response.data
