from flask import Blueprint

bp = Blueprint("home", __name__)

@bp.get("/")
def landing():
    return """
<!doctype html>
<html><body style="font-family:Arial;background:white;">
  <h1>BothStreets</h1>
  <p>See the same story from multiple angles.</p>
  <p><a href="/latest">Latest</a> • <a href="/about">About</a></p>
</body></html>
"""