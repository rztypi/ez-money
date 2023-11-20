def test_change_currency(auth, client, settings):
    auth.login_session()

    response = client.get("/")
    assert b"<option selected>USD</option>" in response.data

    settings.change_currency(currency=None)
    response = client.get("/")
    assert b"Invalid currency." in response.data

    settings.change_currency(currency="not a real currency")
    response = client.get("/")
    assert b"Invalid currency." in response.data

    settings.change_currency(currency="PHP")
    response = client.get("/")
    assert b"<option selected>PHP</option>" in response.data

    settings.change_currency(currency="ZMW")
    response = client.get("/")
    assert b"<option selected>ZMW</option>" in response.data


def test_delete_all(auth, client):
    auth.login_session()

    response = client.get("/")
    assert b"No transactions" not in response.data

    response = client.post("/settings/delete-all", follow_redirects=True)
    assert b"No transactions" in response.data