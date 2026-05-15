from flask import Flask
import os
import pymysql

app = Flask(__name__)

def get_conn():
    return pymysql.connect(
        host=os.environ["MYSQL_HOST"],
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"],
        charset="utf8mb4",
    )

@app.route("/")
def home():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT title, url, source_domain
        FROM articles
        ORDER BY id DESC
        LIMIT 50
    """)
    rows = cur.fetchall()
    conn.close()

    html = ["<html><body style='font-family:Arial;background:white;'>"]
    html.append("<h2>BothStreets – Latest</h2><ul>")
    for title, url, domain in rows:
        html.append(f"<li><a href='{url}' target='_blank'>{title}</a> <small>({domain})</small></li>")
    html.append("</ul></body></html>")
    return "\n".join(html)
