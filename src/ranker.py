"""
Ranking / prioritization for the "Love It" newsletter section.

Scoring factors (all configurable via weights):
  - reaction_bonus:    love reaction = stronger signal than a love comment
  - engagement_score: post's like + comment count (log-scaled, avoids viral outliers dominating)
  - recency_score:    posts from earlier in the week score slightly lower (freshness matters)

Top N posts (default 2) are selected per newsletter edition.
"""

import math
from datetime import datetime, timezone
from models import TaggedPost

# --- Scoring weights (tune as needed) ---
WEIGHTS = {
    "reaction_bonus": 3.0,   # added when Sam used a love reaction (vs. love comment only)
    "engagement": 1.0,       # multiplied by log-scaled engagement
    "recency": 0.5,          # multiplied by recency score (0–1)
}

TOP_N = 2  # posts selected per newsletter edition


def _engagement_score(post) -> float:
    total = post.post_like_count + post.post_comment_count
    return math.log1p(total)  # log(1+x) — smooth curve, handles 0 gracefully


def _recency_score(post, now: datetime) -> float:
    """Linear decay over 7 days. Posts older than 7 days score 0."""
    delta = now - post.timestamp.replace(tzinfo=timezone.utc) if post.timestamp.tzinfo is None else now - post.timestamp
    age_days = delta.total_seconds() / 86400
    return max(0.0, 1.0 - (age_days / 7.0))


def _has_love_reaction(post) -> bool:
    return (post.reaction_type or "").lower() == "love"


def score(tagged_post: TaggedPost, now: datetime | None = None) -> float:
    if now is None:
        now = datetime.now(timezone.utc)
    p = tagged_post.post

    s = 0.0
    if _has_love_reaction(p):
        s += WEIGHTS["reaction_bonus"]

    s += WEIGHTS["engagement"] * _engagement_score(p)
    s += WEIGHTS["recency"] * _recency_score(p, now)
    return round(s, 4)


def rank(tagged_posts: list[TaggedPost], top_n: int = TOP_N, now: datetime | None = None) -> list[TaggedPost]:
    """
    Score and sort tagged posts. Returns top_n posts with scores attached.
    Input should already be filtered to a single tag (e.g. love_it).
    """
    if now is None:
        now = datetime.now(timezone.utc)

    for tp in tagged_posts:
        tp.score = score(tp, now=now)

    return sorted(tagged_posts, key=lambda tp: tp.score, reverse=True)[:top_n]
