from flask import Blueprint

bp = Blueprint("about", __name__)

@bp.get("/about")
def about():
    return """
<!doctype html>
<html><body style="font-family:Arial;background:white;">
  <h2>About</h2>
  <p>Prototype news navigator. Next: add more sources and cluster stories.</p>
  <p><a href="/">Home</a> • <a href="/latest">Latest</a></p>
</body></html>
"""