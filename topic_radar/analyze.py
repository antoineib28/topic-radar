"""Keyword/topic extraction. Works only on aggregates: no usernames, no full posts."""
import json
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

STOPWORDS = set("""
a an the and or but if then so to of in on for with at by from is are was were be been
i me my we you your it its this that these those what how why when where which who
do does did can could should would will just not no yes any some more most very
have has had get got want need know like help about into out up down there here
anyone someone something thing things really also new learn learning program programming
code coding python web dev developer use using way make time one years year day
""".split())

WORD = re.compile(r"[a-zA-Z][a-zA-Z+#.\-]{2,}")


def load_posts(data_dir: Path, start: datetime, end: datetime) -> list[dict]:
    seen, posts = set(), []
    for f in sorted(data_dir.glob("*.json")):
        for p in json.loads(f.read_text()):
            t = datetime.fromtimestamp(p["created_utc"], timezone.utc)
            if start <= t < end and p["id"] not in seen:
                seen.add(p["id"])
                posts.append(p)
    return posts


def keywords(text: str) -> set[str]:
    words = {w.lower().strip(".-") for w in WORD.findall(text)}
    return {w for w in words if w and w not in STOPWORDS}


def topic_counts(posts: list[dict]) -> Counter:
    c = Counter()
    for p in posts:
        c.update(keywords(p["title"] + " " + p["text"]))  # count each topic once per post
    return c


def week_window(weeks_ago: int = 0) -> tuple[datetime, datetime]:
    now = datetime.now(timezone.utc)
    monday = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    start = monday - timedelta(weeks=weeks_ago + 1)
    return start, start + timedelta(weeks=1)
