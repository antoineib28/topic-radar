"""Read-only collection of public posts, with automatic retention cleanup."""
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import praw


def make_client() -> praw.Reddit:
    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"],
    )
    reddit.read_only = True  # never posts, votes or messages
    return reddit


def collect(cfg: dict) -> Path:
    reddit = make_client()
    data_dir = Path(cfg["data_dir"])
    data_dir.mkdir(exist_ok=True)

    rows = []
    for name in cfg["subreddits"]:
        for post in reddit.subreddit(name).new(limit=cfg["posts_per_subreddit"]):
            # No author / profile data is stored.
            rows.append({
                "id": post.id,
                "subreddit": name,
                "title": post.title,
                "text": post.selftext,
                "score": post.score,
                "num_comments": post.num_comments,
                "created_utc": post.created_utc,
            })

    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out = data_dir / f"{day}.json"
    out.write_text(json.dumps(rows, ensure_ascii=False))
    purge_old(data_dir, cfg["retention_days"])
    return out


def purge_old(data_dir: Path, retention_days: int) -> None:
    cutoff = time.time() - retention_days * 86400
    for f in data_dir.glob("*.json"):
        if f.stat().st_mtime < cutoff:
            f.unlink()
