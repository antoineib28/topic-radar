"""Weekly Markdown report containing aggregate statistics only."""
from pathlib import Path

from .analyze import load_posts, topic_counts, week_window


def write_report(cfg: dict) -> Path:
    data_dir, reports_dir = Path(cfg["data_dir"]), Path(cfg["reports_dir"])
    reports_dir.mkdir(exist_ok=True)

    start, end = week_window(0)
    prev_start, prev_end = week_window(1)
    posts = load_posts(data_dir, start, end)
    current = topic_counts(posts)
    previous = topic_counts(load_posts(data_dir, prev_start, prev_end))

    year, week, _ = start.isocalendar()
    lines = [
        f"# Topic Radar – week {week}, {year}",
        "",
        f"Period: {start:%Y-%m-%d} to {end:%Y-%m-%d} · {len(posts)} public posts analysed "
        f"in {', '.join('r/' + s for s in cfg['subreddits'])}.",
        "",
        "| # | Topic | Posts | vs last week |",
        "|---|---|---|---|",
    ]
    for i, (topic, n) in enumerate(current.most_common(cfg["top_n"]), 1):
        delta = n - previous.get(topic, 0)
        lines.append(f"| {i} | {topic} | {n} | {delta:+d} |")
    lines += ["", "_Aggregate counts only. No usernames or post contents are published._", ""]

    out = reports_dir / f"{year}-W{week:02d}.md"
    out.write_text("\n".join(lines))
    return out
