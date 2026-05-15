import json
import sqlite3   
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT /"data"/ "news.db"
OUT_PATH = PROJECT_ROOT /"data" / "articles.json"

def export_latest(limit: int =300):
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    
    cur.execute("""
        SELECT id, source_domain, title, url, published_at, fetched_at
        FROM articles
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()

    articles = [
        {
            "id": r[0],
            "source_domain": r[1],
            "title": r[2],
            "url": r[3],
            "published_art": r[4],
            "fetched_at": r[5]
        }
        for r in rows
    ]

    OUT_PATH.write_text(
    json.dumps(articles, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

    print(f"Exported {len(articles)} articles → {OUT_PATH} ")

if __name__ == "__main__":
    export_latest(limit=300)