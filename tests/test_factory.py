from ezmoney import create_app


def test_config():
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_route(client, auth):
    auth.login_session()
    response = client.get("/test")
    assert response.data == b"<h1>What's up, hello_world@gmail.com?</h1>"