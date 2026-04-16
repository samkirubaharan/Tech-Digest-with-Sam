"""
Tagging engine for the Tech Digest newsletter framework.

Applies section tags to LinkedIn posts based on Sam's interactions.
"""

import re
from models import LinkedInPost, TaggedPost

# Phrases that signal genuine love in a comment (case-insensitive)
LOVE_COMMENT_PATTERNS = [
    r"\blove (this|it|post|article|piece|thread|take|perspective|insight)\b",
    r"\bi love\b",
    r"\bthis is (so )?lovely\b",
    r"\babsolutely love\b",
    r"\bjust love\b",
]

_LOVE_RE = re.compile("|".join(LOVE_COMMENT_PATTERNS), re.IGNORECASE)


def _is_love_reaction(post: LinkedInPost) -> bool:
    return (post.reaction_type or "").lower() == "love"


def _is_love_comment(post: LinkedInPost) -> bool:
    if not post.comment_text:
        return False
    return bool(_LOVE_RE.search(post.comment_text))


def tag_post(post: LinkedInPost) -> TaggedPost:
    """Return a TaggedPost with all applicable section tags."""
    tags = []

    if _is_love_reaction(post) or _is_love_comment(post):
        tags.append("love_it")

    return TaggedPost(post=post, tags=tags)


def tag_all(posts: list[LinkedInPost]) -> list[TaggedPost]:
    """Tag a list of posts. Returns all posts (tagged and untagged)."""
    return [tag_post(p) for p in posts]


def filter_by_tag(tagged: list[TaggedPost], tag: str) -> list[TaggedPost]:
    """Return only posts that have a specific tag."""
    return [t for t in tagged if tag in t.tags]
