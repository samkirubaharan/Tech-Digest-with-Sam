"""
Unit tests for the tagging + ranking pipeline.
Run with: python tests.py
"""

import sys
from datetime import datetime, timezone, timedelta
from models import LinkedInPost
from tagger import tag_post, tag_all, filter_by_tag
from ranker import rank, score


def make_post(
    post_id="p1",
    reaction_type=None,
    comment_text=None,
    post_like_count=100,
    post_comment_count=10,
    days_ago=1,
):
    ts = datetime.now(timezone.utc) - timedelta(days=days_ago)
    return LinkedInPost(
        post_id=post_id,
        author_name="Test Author",
        author_headline="CEO at TestCo",
        post_text="Some interesting post about AI.",
        post_url="https://linkedin.com/posts/test",
        timestamp=ts,
        reaction_type=reaction_type,
        comment_text=comment_text,
        post_like_count=post_like_count,
        post_comment_count=post_comment_count,
    )


def test_love_reaction_tags():
    tp = tag_post(make_post(reaction_type="love"))
    assert "love_it" in tp.tags, "love reaction should tag love_it"

def test_love_comment_tags():
    tp = tag_post(make_post(comment_text="I love this post!"))
    assert "love_it" in tp.tags

def test_love_comment_variety():
    phrases = [
        "I love it",
        "absolutely love this",
        "just love this perspective",
        "love this article",
        "this is lovely",
    ]
    for phrase in phrases:
        tp = tag_post(make_post(comment_text=phrase))
        assert "love_it" in tp.tags, f"Should tag love_it for: '{phrase}'"

def test_like_reaction_does_not_tag():
    tp = tag_post(make_post(reaction_type="like"))
    assert "love_it" not in tp.tags, "like reaction should NOT tag love_it"

def test_unrelated_comment_does_not_tag():
    tp = tag_post(make_post(comment_text="Great point, totally agree!"))
    assert "love_it" not in tp.tags

def test_no_interaction_does_not_tag():
    tp = tag_post(make_post())
    assert tp.tags == []

def test_rank_returns_top_n():
    posts = [
        make_post("p1", reaction_type="love", post_like_count=500, days_ago=1),
        make_post("p2", reaction_type="love", post_like_count=200, days_ago=2),
        make_post("p3", reaction_type="love", post_like_count=50,  days_ago=3),
    ]
    tagged = filter_by_tag(tag_all(posts), "love_it")
    top = rank(tagged, top_n=2)
    assert len(top) == 2

def test_rank_orders_by_score():
    posts = [
        make_post("low",  reaction_type="love", post_like_count=10,   days_ago=6),
        make_post("high", reaction_type="love", post_like_count=5000, days_ago=1),
    ]
    tagged = filter_by_tag(tag_all(posts), "love_it")
    top = rank(tagged, top_n=2)
    assert top[0].post.post_id == "high", "higher-engagement recent post should rank first"

def test_reaction_bonus_beats_comment_only():
    now = datetime.now(timezone.utc)
    p_react  = make_post("r", reaction_type="love",  comment_text=None, post_like_count=100, days_ago=1)
    p_comment = make_post("c", reaction_type=None,   comment_text="I love this", post_like_count=100, days_ago=1)
    from tagger import tag_post as tp_fn
    tr = tp_fn(p_react)
    tc = tp_fn(p_comment)
    assert score(tr, now=now) > score(tc, now=now), "love reaction should outscore love comment at same engagement"

def test_old_post_lower_score():
    now = datetime.now(timezone.utc)
    fresh = make_post("f", reaction_type="love", days_ago=1)
    stale = make_post("s", reaction_type="love", days_ago=6)
    from tagger import tag_post as tp_fn
    assert score(tp_fn(fresh), now=now) > score(tp_fn(stale), now=now)

def test_rank_fewer_than_n_posts():
    posts = [make_post("only", reaction_type="love")]
    tagged = filter_by_tag(tag_all(posts), "love_it")
    top = rank(tagged, top_n=2)
    assert len(top) == 1, "should return all available posts if fewer than top_n"


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    passed = failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL  {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ERROR {t.__name__}: {e}")
            failed += 1

    print(f"\n{passed}/{passed+failed} tests passed.")
    sys.exit(0 if failed == 0 else 1)
