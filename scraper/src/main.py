import time
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from scraper.db import get_connection  # <-- NEW #Updated 5/15/26

HEADERS = {
    "User-Agent": "BothStreetsBot/0.1 (local dev)"
}

SEED_URLS = [
    "https://www.cnn.com/",
]

VIDEO_URLS = ["/video", "/videos", "video", "watch", "/tv", "/live"]
VIDEO_TITLES = ["video", "watch"]

def is_video_link(title: str, url: str) -> bool:
    t = title.lower()
    u = url.lower()
    return any(word in u for word in VIDEO_URLS) or any(word in t for word in VIDEO_TITLES)

def ensure_db():
    """
    Create the MySQL table if it doesn't exist.
    Note: UNIQUE on a TEXT column requires an index prefix in MySQL, so we use url(255).
    """
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                source_domain VARCHAR(255) NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                published_at DATETIME NULL,
                fetched_at DATETIME NOT NULL,
                UNIQUE KEY unique_url (url(255))
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        """)
    conn.close()

def same_domain(url_a: str, url_b: str) -> bool:
    return urlparse(url_a).netloc == urlparse(url_b).netloc

def scrape_listing(seed_url: str):
    r = requests.get(seed_url, headers=HEADERS, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")
    items = []

    for a in soup.select("a"):
        title = (a.get_text() or "").strip()
        href = a.get("href")

        if not href or not title:
            continue

        if len(title) < 25:
            continue

        url = urljoin(seed_url, href)

        if is_video_link(title, url):
            continue

        if not same_domain(url, seed_url):
            continue

        items.append({
            "source_domain": urlparse(seed_url).netloc,
            "title": title[:300],
            "url": url,
            "published_at": None,
            "fetched_at": datetime.now(timezone.utc),  # store as datetime for MySQL DATETIME
        })

    # De-dupe by URL in-memory
    seen = set()
    deduped = []
    for it in items:
        if it["url"] in seen:
            continue
        seen.add(it["url"])
        deduped.append(it)

    return deduped

def save_articles(articles):
    """
    Insert into MySQL. Use %s placeholders (MySQL style).
    Uses INSERT IGNORE to skip duplicates caused by UNIQUE(url(255)).
    """
    if not articles:
        return 0

    conn = get_connection()
    inserted = 0

    with conn.cursor() as cur:
        for a in articles:
            cur.execute("""
                INSERT IGNORE INTO articles (source_domain, title, url, published_at, fetched_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (a["source_domain"], a["title"], a["url"], a["published_at"], a["fetched_at"]))

            # rowcount: 1 if inserted, 0 if ignored
            if cur.rowcount == 1:
                inserted += 1

    conn.close()
    return inserted

def main():
    ensure_db()

    total_inserted = 0
    for seed in SEED_URLS:
        print(f"Scraping: {seed}")
        articles = scrape_listing(seed)
        inserted = save_articles(articles)
        total_inserted += inserted
        print(f"  found={len(articles)} inserted={inserted}")
        time.sleep(2)

    print(f"Done. Total inserted: {total_inserted}")

if __name__ == "__main__":
    main()
