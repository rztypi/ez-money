from ezmoney.helpers import validate_amount, validate_description, validate_date, format_currency, text_color


def test_validate_amount():
    assert not validate_amount("")
    assert not validate_amount(" ")
    assert not validate_amount("123.123")
    assert not validate_amount("0.001")
    assert not validate_amount("1.1.1")
    assert not validate_amount("thisshouldbewrong")
    assert not validate_amount("1000000000.01")
    assert not validate_amount("-1000000000.01")
    assert validate_amount("100.00")
    assert validate_amount("0")
    assert validate_amount("48")
    assert validate_amount("0.66")
    assert validate_amount("1000000000")
    assert validate_amount("-1000000000")


def test_validate_description():
    assert not validate_description("")
    assert not validate_description(" ")
    assert validate_description("     h     ")
    assert validate_description("hello")


def test_validate_date():
    assert not validate_date("")
    assert not validate_date(" ")
    assert not validate_date("thisisnotadate")
    assert not validate_date("9999-12-12")
    assert validate_date("2012-12-12")


def test_format_currency(client, auth, settings):
    auth.login_session()

    with client:
        client.get("/")
        assert format_currency(100) == "$100.00"
        assert format_currency(-100) == "$100.00"
        assert format_currency(0) == "$0.00"
        assert format_currency(0.11111) == "$0.11"
        assert format_currency(-0.1) == "$0.10"

        settings.change_currency(currency="PHP")
        client.get("/")
        assert format_currency(100, with_sign=True) == "+ ₱100.00"
        assert format_currency(-100, with_sign=True) == "- ₱100.00"
        assert format_currency(0, with_sign=True) == "₱0.00"
        assert format_currency(0.11111, with_sign=True) == "+ ₱0.11"
        assert format_currency(-0.1, with_sign=True) == "- ₱0.10"



def test_text_color():
    assert text_color(1) == "text-success"
    assert text_color(-1) == "text-danger"
    assert text_color(0) == ""