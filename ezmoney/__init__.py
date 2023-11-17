import os
from datetime import date

from dotenv import load_dotenv
from flask import Flask, g


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    load_dotenv()
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "this_was_sc50"),
        DATABASE=os.path.join(app.instance_path, "ez-money.sqlite"),
        GOOGLE_CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID", "client_id_here"),
        GOOGLE_CLIENT_SECRET=os.getenv("GOOGLE_CLIENT_SECRET", "client_secret_here"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
    auth.init_oauth(app)

    from . import transaction
    app.register_blueprint(transaction.bp)
    app.add_url_rule("/", endpoint="index")

    from . import helpers
    app.jinja_env.filters["abs_currency"] = helpers.abs_currency
    app.jinja_env.filters["currency"] = helpers.currency
    app.jinja_env.filters["text_color"] = helpers.text_color

    @app.context_processor
    def inject_date():
        return dict(date=date)

    @app.route("/test")
    @auth.login_required
    def test():
        return f"<h1>What's up, {g.user['email']}?</h1>"
    
    return app