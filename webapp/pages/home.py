from flask import Blueprint, render_template

bp = Blueprint("home", __name__)

@bp.get("/")
def landing():
    return render_template("home.html")