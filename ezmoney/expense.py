from datetime import date

from flask import Blueprint, redirect, render_template, url_for, g, request, flash

from ezmoney.auth import login_required
from ezmoney.db import get_db
from ezmoney.helpers import validate_amount, validate_description, validate_date


bp = Blueprint("expense", __name__)


@bp.route("/", methods=("GET", "POST"))
def index():
    db = get_db()
    expenses = []
    total = None

    if g.user_id is not None:
        expenses = db.execute(
            "SELECT * FROM expense WHERE user_id = ? ORDER BY id DESC",
            (g.user_id,),
        ).fetchall()
        total = sum(expense["amount"] for expense in expenses)

    return render_template("expense/index.html", expenses=expenses, total=total)


@bp.route("/add", methods=("POST",))
@login_required
def add():
    amount = request.form.get("amount")
    description = request.form.get("description")
    created = request.form.get("date")
    error = None

    if not amount:
        error = "Amount must be provided."
    elif not description:
        error = "Description must be provided."
    elif not created:
        error = "Date must be provided."
    elif not validate_amount(amount):
        error = "Invalid amount."
    elif not validate_description(description):
        error = "Invalid description."
    elif not validate_date(created):
        error = "Invalid date."

    if error is None:
        db = get_db()
        db.execute(
            """
            INSERT INTO expense (user_id, description, amount, created)
            VALUES (?, ?, ?, ?)
            """,
            (
                g.user_id,
                description.strip(),
                float(amount),
                created
            ),
        )
        db.commit()
    else:
        flash(error, "warning")

    return redirect(url_for("index"))


@bp.route("/edit/<int:id>", methods=("POST",))
@login_required
def edit(id):
    amount = request.form.get("amount")
    description = request.form.get("description")
    created = request.form.get("date")
    db = get_db()
    expense = db.execute(
        "SELECT * FROM expense WHERE id = ? AND user_id = ?", (id, g.user_id)
    ).fetchone()
    error = None

    if not amount:
        error = "Amount must be provided."
    elif not description:
        error = "Description must be provided."
    elif not created:
        error = "Date must be provided."
    elif not validate_amount(amount):
        error = "Invalid amount."
    elif not validate_description(description):
        error = "Invalid description."
    elif not validate_date(created):
        error = "Invalid date."
    elif expense is None:
        error = "Expense does not exist."

    if error is None:
        db.execute(
            """
            UPDATE expense
            SET description = ?, amount = ?, created = ?
            WHERE id = ?
            """,
            (
                description.strip(),
                float(amount),
                created,
                id,
            ),
        )
        db.commit()
        flash("Success!", "success")
    else:
        flash(error, "warning")
    return redirect(url_for("index"))


@bp.route("/delete/<int:id>", methods=("POST",))
@login_required
def delete(id):
    db = get_db()
    expense = db.execute(
        "SELECT * FROM expense WHERE id = ? AND user_id = ?", (id, g.user_id)
    ).fetchone()

    if expense is not None:
        db.execute("DELETE FROM expense WHERE id = ?", (id,))
        db.commit()
        flash("Deleted.", "success")
    else:
        flash("Expense cannot be deleted.", "warning")

    return redirect(url_for("index"))
