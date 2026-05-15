from flask import Blueprint
from webapp.db import get_conn

bp = Blueprint("latest", __name__)

@bp.get("/latest")
def latest():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT title, url, source_domain
        FROM articles
        ORDER BY id DESC
        LIMIT 75
    """)
    rows = cur.fetchall()
    conn.close()

    items = "".join(
        f"<li><a href='{url}' target='_blank' rel='noreferrer'>{title}</a> <small>({domain})</small></li>"
        for title, url, domain in rows
    )

    return f"""
<!doctype html>
<html><body style="font-family:Arial;background:white;">
  <h2>Latest</h2>
  <p><a href="/">Home</a> • <a href="/about">About</a></p>
  <ul>{items or "<li>No articles yet.</li>"}</ul>
</body></html>
"""