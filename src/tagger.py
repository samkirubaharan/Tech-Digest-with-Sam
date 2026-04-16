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

# ---------------------------------------------------------------------------
# Mr. & Mrs. Curious — Sam disagrees, questions, or redirects the convo.
# Covers everything from direct pushback to exploratory alternatives.
# ---------------------------------------------------------------------------
CURIOUS_COMMENT_PATTERNS = [
    # Direct disagreement / pushback
    r"\bi disagree\b",
    r"\bi don'?t think so\b",
    r"\bi don'?t buy (this|that)\b",
    r"\bi (strongly )?(disagree|push back)\b",
    r"\bi('d| would) (push back|pushback)\b",
    r"\bnot sure i (fully )?agree\b",
    r"\bi('d| would) challenge (this|that)\b",
    r"\brespectfully (disagree|i disagree)\b",
    r"\bthis (misses|overlooks|ignores) the (point|mark|bigger picture)\b",
    r"\bthat'?s (not right|incorrect|misleading|overstated|oversimplified)\b",
    r"\bi think (this is|that'?s) (wrong|off|misleading|overstated|too simplistic)\b",
    r"\bthe (data|evidence|research) (doesn'?t|don'?t) (support|back)\b",
    # Alternative framing / redirect
    r"\bi('d| would) argue\b",
    r"\bi('d| would) suggest\b",
    r"\balternatively\b",
    r"\bwhat if instead\b",
    r"\ba different (take|angle|view|perspective)\b",
    r"\bon the other hand\b",
    r"\bactually[,.]? i\b",
    # Curious challenge / questioning
    r"\bhave you considered\b",
    r"\bwhat about\b",
    r"\bi wonder if\b",
    r"\bwouldn'?t it (be|make more sense)\b",
    r"\bbut (what if|couldn'?t)\b",
]

_CURIOUS_RE = re.compile("|".join(CURIOUS_COMMENT_PATTERNS), re.IGNORECASE)


def _is_love_reaction(post: LinkedInPost) -> bool:
    return (post.reaction_type or "").lower() == "love"


def _is_love_comment(post: LinkedInPost) -> bool:
    if not post.comment_text:
        return False
    return bool(_LOVE_RE.search(post.comment_text))


def _is_curious_comment(post: LinkedInPost) -> bool:
    """Sam disagreed, questioned, or offered an alternative in his comment."""
    if not post.comment_text:
        return False
    return bool(_CURIOUS_RE.search(post.comment_text))


# ---------------------------------------------------------------------------
# Incoming — reposts of new release announcements or GitHub repo shares.
# Requires BOTH: Sam reposted it AND content matches a release or repo signal.
# ---------------------------------------------------------------------------
RELEASE_PATTERNS = [
    r"\bannouncing\b",
    r"\bjust (launched|released|shipped|dropped|published)\b",
    r"\bnow (available|live|open[ -]source)\b",
    r"\bintroducing\b",
    r"\bnew release\b",
    r"\bv\d+\.\d+",                          # version strings e.g. v2.1, v0.9.3
    r"\blaunch(ing|ed)?\b",
    r"\bopen[ -]sourc(ing|ed)\b",
    r"\brelease candidate\b",
    r"\bgeneral availability\b",
    r"\bga release\b",
]

GITHUB_PATTERNS = [
    r"github\.com/[\w\-]+/[\w\-]+",          # github.com/org/repo
    r"\bgithub repo\b",
    r"\bopen[ -]source(d)? (repo|project|tool|library|framework)\b",
]

_RELEASE_RE = re.compile("|".join(RELEASE_PATTERNS), re.IGNORECASE)
_GITHUB_RE  = re.compile("|".join(GITHUB_PATTERNS),  re.IGNORECASE)


def _is_release_content(post: LinkedInPost) -> bool:
    return bool(_RELEASE_RE.search(post.post_text))


def _is_github_content(post: LinkedInPost) -> bool:
    return bool(_GITHUB_RE.search(post.post_text))


def _is_incoming(post: LinkedInPost) -> bool:
    """Repost of a new release announcement or a GitHub repo share."""
    if not post.is_repost:
        return False
    return _is_release_content(post) or _is_github_content(post)


# ---------------------------------------------------------------------------
# The Byline — Sam's own original articles/posts.
# PLACEHOLDER: currently detects via the is_own_post flag in the data.
# TODO: confirm how Sam's LinkedIn export distinguishes authored posts from
#       activity on others' posts, and update the signal here accordingly.
# ---------------------------------------------------------------------------
def _is_own_article(post: LinkedInPost) -> bool:
    """Returns True when the post is Sam's own original content."""
    return post.is_own_post


def tag_post(post: LinkedInPost) -> TaggedPost:
    """Return a TaggedPost with all applicable section tags."""
    tags = []

    if _is_love_reaction(post) or _is_love_comment(post):
        tags.append("love_it")

    if _is_curious_comment(post):
        tags.append("mr_mrs_curious")

    if _is_own_article(post):
        tags.append("the_byline")

    if _is_incoming(post):
        tags.append("incoming")

    return TaggedPost(post=post, tags=tags)


def tag_all(posts: list[LinkedInPost]) -> list[TaggedPost]:
    """Tag a list of posts. Returns all posts (tagged and untagged)."""
    return [tag_post(p) for p in posts]


def filter_by_tag(tagged: list[TaggedPost], tag: str) -> list[TaggedPost]:
    """Return only posts that have a specific tag."""
    return [t for t in tagged if tag in t.tags]
