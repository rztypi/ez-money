import functools

from flask import (
    Blueprint,
    g,
    redirect,
    session,
    url_for,
)
from authlib.integrations.flask_client import OAuth


bp = Blueprint("auth", __name__, url_prefix="/auth")
oauth = OAuth()


@bp.route("/login")
def login():
    redirect_uri = url_for("auth.authorize", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@bp.route("/authorize")
def authorize():
    token = oauth.google.authorize_access_token()
    session["user_email"] = token["userinfo"]["email"]
    return redirect(url_for("index"))


@bp.before_app_request
def load_logged_in_user():
    g.user_email = session.get("user_email")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user_email is None:
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
