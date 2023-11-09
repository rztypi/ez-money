from datetime import date, timedelta

from flask import Blueprint, redirect, render_template, url_for, g, request, flash, session

from ezmoney.auth import login_required
from ezmoney.db import get_db
from ezmoney.helpers import validate_amount, validate_description, validate_date


bp = Blueprint("expense", __name__)


@bp.route("/", methods=("GET", "POST"))
def index():
    expenses = None
    chart = None
    db = get_db()

    if g.user_id is not None:
        t = request.args.get("t")
        time_diff = {
            "week": "-7 days",
            "month": "-30 days",
            "year": "-365 days",
        }
        
        # Get expenses
        if t in time_diff:
            expenses = db.execute(
                "SELECT * FROM expense WHERE user_id = ? AND created >= date('now', ?) ORDER BY created",
                (g.user_id, time_diff[t])
            ).fetchall()
            session["t"] = t
        else:
            expenses = db.execute(
                "SELECT * FROM expense WHERE user_id = ? ORDER BY created",
                (g.user_id,),
            ).fetchall()
            session["t"] = None
        
        # Get chart data if there are expenses
        if expenses is not None:
            chart = {
                "labels": [],
                "data": [],
            }

            days_ago = 7

            if t == "month":
                days_ago = 30
            if t == "year":
                days_ago = 365
            
            for i in range(days_ago, -1, -1):
                chart["labels"].append(i)

                expense = db.execute(
                    "SELECT SUM(amount) AS amount FROM expense WHERE user_id = ? AND created = ?",
                    (
                        g.user_id, 
                        date.today() - timedelta(days=i),
                    )
                ).fetchone()
                amount = 0 if expense["amount"] is None else expense["amount"]
                chart["data"].append(amount)

    return render_template("expense/index.html", expenses=expenses, chart=chart)


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
                created,
            ),
        )
        db.commit()
    else:
        flash(error, "warning")

    return redirect(url_for("index", t=session.get("t")))


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

    return redirect(url_for("index", t=session.get("t")))


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

    return redirect(url_for("index", t=session.get("t")))
