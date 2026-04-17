"""
Data models for the Tech Digest newsletter framework.

Expected LinkedIn export format (list of dicts or JSON array):
[
  {
    "post_id": "urn:li:activity:123456",
    "author_name": "Jane Smith",
    "author_headline": "AI Researcher at DeepMind",
    "post_text": "...",
    "post_url": "https://www.linkedin.com/posts/...",
    "timestamp": "2026-04-10T14:32:00Z",
    "reaction_type": "love",          # null if no reaction
    "comment_text": null,             # null if no comment
    "post_like_count": 420,
    "post_comment_count": 38,
    "is_own_post": false,             # true when this is Sam's own original article/post
    "is_repost": false                # true when Sam reposted/reshared someone else's content
  },
  ...
]
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class LinkedInPost:
    post_id: str
    author_name: str
    post_text: str
    post_url: str
    timestamp: datetime
    author_headline: str = ""
    reaction_type: Optional[str] = None   # e.g. "love", "like", "celebrate"
    comment_text: Optional[str] = None
    post_like_count: int = 0
    post_comment_count: int = 0
    is_own_post: bool = False              # True when this is Sam's own original article/post
    is_repost: bool = False                # True when Sam reposted/reshared someone else's content
    tags: list = field(default_factory=list)


@dataclass
class TaggedPost:
    post: LinkedInPost
    tags: list[str]
    score: float = 0.0
