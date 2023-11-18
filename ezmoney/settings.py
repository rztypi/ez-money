from flask import Blueprint, g, request, flash, redirect, url_for
from currencies import Currency, CurrencyDoesNotExist

from ezmoney.db import get_db


bp = Blueprint("settings", __name__, url_prefix="/settings")


@bp.route("/change-currency", methods=("POST",))
def change_currency():
    currency = request.form.get("currency")
    error = None
    
    try:
        Currency(currency)
    except CurrencyDoesNotExist:
        error = "Invalid currency."

    if error is None:
        db = get_db()
        db.execute(
            """
            UPDATE user
            SET currency = ?
            WHERE id = ?
            """,
            (
                currency,
                g.user_id
            )
        )
        db.commit()
        flash(f"Currency changed to {currency}.", "success")
    else:
        flash(error, "warning")

    return redirect(url_for("index"))