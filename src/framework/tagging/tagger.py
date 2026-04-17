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


# ---------------------------------------------------------------------------
# Trending — GitHub projects Sam interacted with (any reaction, comment, repost).
# Stricter than Incoming: requires a real github.com/org/repo URL.
# Ranking (in ranker.py) weights engagement heavily to surface what's blowing up.
# ---------------------------------------------------------------------------
_GITHUB_URL_RE = re.compile(r"github\.com/[\w\-\.]+/[\w\-\.]+", re.IGNORECASE)


def _has_github_url(post: LinkedInPost) -> bool:
    return bool(_GITHUB_URL_RE.search(post.post_text))


def _has_any_interaction(post: LinkedInPost) -> bool:
    return bool(post.reaction_type or post.comment_text or post.is_repost)


def _is_trending(post: LinkedInPost) -> bool:
    """GitHub project post that Sam interacted with in any way."""
    return _has_github_url(post) and _has_any_interaction(post)


# ---------------------------------------------------------------------------
# Reflection — posts about AI governance, regulation, or negative societal
# effects that Sam engaged with.  Any interaction qualifies (Sam choosing to
# react or comment signals the post gave him pause).
# ---------------------------------------------------------------------------
REFLECTION_PATTERNS = [
    # Governance & regulation
    r"\bai governance\b",
    r"\bai regulation\b",
    r"\bai policy\b",
    r"\bai oversight\b",
    r"\bai legislation\b",
    r"\bregulat(e|ing|ion of) ai\b",
    r"\bai act\b",
    r"\bresponsible ai\b",
    r"\bai ethics\b",
    r"\bethical ai\b",
    r"\bai accountability\b",
    r"\bai transparency\b",
    # Safety & risk
    r"\bai safety\b",
    r"\bai alignment\b",
    r"\bai risk\b",
    r"\bexistential risk\b",
    r"\bai (is )?(moving )?too fast\b",
    r"\bpause ai\b",
    r"\bai moratorium\b",
    r"\bfrontier (ai )?risk\b",
    # Negative societal effects
    r"\bjob (displacement|loss(es)?|cut(s|ting)?)\b.*\bai\b",
    r"\bai.*\bjob (displacement|loss(es)?|cut(s|ting)?)\b",
    r"\breplac(e|ing) (human|worker|job)s?\b",
    r"\bautomation (layoff|job loss|unemployment)\b",
    r"\bai bias\b",
    r"\balgorithmic bias\b",
    r"\bdiscriminat(ory|ion).{0,30}ai\b",
    r"\bai.{0,30}discriminat(ory|ion)\b",
    r"\bdeepfakes?\b",
    r"\bai misinformation\b",
    r"\bai disinformation\b",
    r"\bsynthetic media\b",
    r"\bai surveillance\b",
    r"\bfacial recognition\b",
    r"\bautonomous weapons?\b",
    r"\bai weapon\b",
    r"\bunintended consequences.{0,30}ai\b",
    r"\bai.{0,30}unintended consequences\b",
    r"\bdark side of ai\b",
    r"\bdangers? of ai\b",
    r"\bai harm\b",
    r"\bai (is )?not ready\b",
    r"\bwe need to (talk|think) about ai\b",
]

_REFLECTION_RE = re.compile("|".join(REFLECTION_PATTERNS), re.IGNORECASE)


def _is_reflection(post: LinkedInPost) -> bool:
    """Post touches AI governance or negative AI effects and Sam interacted."""
    if not _has_any_interaction(post):
        return False
    return bool(_REFLECTION_RE.search(post.post_text))


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

    if _is_trending(post):
        tags.append("trending")

    if _is_reflection(post):
        tags.append("reflection")

    return TaggedPost(post=post, tags=tags)


def tag_all(posts: list[LinkedInPost]) -> list[TaggedPost]:
    """Tag a list of posts. Returns all posts (tagged and untagged)."""
    return [tag_post(p) for p in posts]


def filter_by_tag(tagged: list[TaggedPost], tag: str) -> list[TaggedPost]:
    """Return only posts that have a specific tag."""
    return [t for t in tagged if tag in t.tags]
