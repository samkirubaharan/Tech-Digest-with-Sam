"""
Loads LinkedIn activity data from a JSON file into LinkedInPost objects.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from models import LinkedInPost


def load(path: str | Path) -> list[LinkedInPost]:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)

    posts = []
    for item in raw:
        ts = item.get("timestamp")
        if isinstance(ts, str):
            ts = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        elif ts is None:
            ts = datetime.now(timezone.utc)

        posts.append(LinkedInPost(
            post_id=item.get("post_id", ""),
            author_name=item.get("author_name", ""),
            author_headline=item.get("author_headline", ""),
            post_text=item.get("post_text", ""),
            post_url=item.get("post_url", ""),
            timestamp=ts,
            reaction_type=item.get("reaction_type"),
            comment_text=item.get("comment_text"),
            post_like_count=item.get("post_like_count", 0),
            post_comment_count=item.get("post_comment_count", 0),
        ))

    return posts
