# Topic Radar

**What do beginners keep asking about?** Topic Radar is a small, open-source, non-commercial tool that produces a weekly report of the most frequently discussed topics in programming-learning communities on Reddit:

- r/learnprogramming
- r/learnpython
- r/webdev

The goal is to help these communities (members, wiki maintainers and moderators) see which questions come up again and again, so that FAQs, wikis and learning resources can focus on what people actually need.

## What it does

1. Once a day, it reads the newest **public** posts from the three subreddits above (title, body text, score, number of comments, creation date).
2. It extracts keywords and groups them into topics (e.g. "recursion", "first job", "React vs Vue").
3. Once a week, it publishes an **aggregated** report in [`reports/`](reports/): the top topics and how they evolved compared with the previous week.

## What it does NOT do

- It is **read-only**: it never posts, comments, votes, sends messages or performs moderation actions.
- It does **not** collect or publish usernames, profile data or full posts. Reports contain only aggregate counts and keywords.
- It does **not** sell or share data, and the data is **not** used to train AI models.
- It is not commercial.

## Responsible use of Reddit data

| Topic | How it's handled |
|---|---|
| Access | Official Reddit Data API via [PRAW](https://praw.readthedocs.io/), read-only scope |
| Volume | About 3 requests per day, far below the rate limit |
| User-Agent | `script:topic-radar:v1.0 (by /u/<username>)` |
| Retention | Raw data is kept locally for at most **30 days**, then deleted automatically (`retention_days` in `config.toml`) |
| Deletions | Each run re-fetches current data, so posts deleted or removed on Reddit are not kept |
| Policy | Follows Reddit's Responsible Builder Policy, Developer Terms and Data API Terms |

## Why not Devvit?

Devvit apps run inside Reddit and are designed for in-platform experiences. Topic Radar needs scheduled offline text analysis with Python libraries, and its output (Markdown reports and charts) is hosted on GitHub, outside Reddit.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in your Reddit API credentials
python -m topic_radar collect   # daily: fetch new posts
python -m topic_radar report    # weekly: write reports/YYYY-WW.md
```

## Project structure

```
topic_radar/
  collect.py   # read-only fetch of public posts + retention cleanup
  analyze.py   # keyword/topic extraction and aggregation
  report.py    # weekly Markdown report
  __main__.py  # command-line entry point
config.toml    # subreddits, limits, retention
reports/       # published weekly reports (aggregates only)
```

## License

MIT
