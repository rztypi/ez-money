import functools

from flask import Blueprint, g, redirect, session, url_for

from authlib.integrations.flask_client import OAuth

from ezmoney.db import get_db


bp = Blueprint("auth", __name__, url_prefix="/auth")
oauth = OAuth()


@bp.route("/login")
def login():
    redirect_uri = url_for("auth.authorize", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@bp.route("/authorize")
def authorize():
    token = oauth.google.authorize_access_token()
    session["user_id"] = token["userinfo"]["sub"]
    save_user(token["userinfo"])
    return redirect(url_for("index"))


def save_user(userinfo):
    db = get_db()
    user = db.execute("SELECT * FROM user WHERE id = ?", (userinfo["sub"],)).fetchone()

    if user is None:
        db.execute(
            """
            INSERT INTO user (id, email, given_name, family_name)
            VALUES (?, ?, ?, ?)
            """,
            (
                userinfo["sub"],
                userinfo["email"],
                userinfo["given_name"],
                userinfo["family_name"],
            )
        )
        db.commit()


@bp.before_app_request
def load_logged_in_user():
    g.user_id = session.get("user_id")
    g.user = None

    if g.user_id is not None:
        g.user = get_db().execute("SELECT * FROM user WHERE id = ?", (g.user_id,)).fetchone()


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user_id is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


def init_oauth(app):
    oauth.init_app(app)
    oauth.register(
        name="google",
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid profile email"},
    )
