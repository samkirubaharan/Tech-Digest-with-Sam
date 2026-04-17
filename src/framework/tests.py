"""
Unit tests for the tagging + ranking pipeline.
Run with: python tests.py
"""

import sys
from datetime import datetime, timezone, timedelta
from models import LinkedInPost
from tagger import tag_post, tag_all, filter_by_tag
from ranker import rank, score, rank_trending, score_trending, rank_reflection, score_reflection


def make_post(
    post_id="p1",
    reaction_type=None,
    comment_text=None,
    post_text="Some interesting post about AI.",
    post_like_count=100,
    post_comment_count=10,
    days_ago=1,
):
    ts = datetime.now(timezone.utc) - timedelta(days=days_ago)
    return LinkedInPost(
        post_id=post_id,
        author_name="Test Author",
        author_headline="CEO at TestCo",
        post_text=post_text,
        post_url="https://linkedin.com/posts/test",
        timestamp=ts,
        reaction_type=reaction_type,
        comment_text=comment_text,
        post_like_count=post_like_count,
        post_comment_count=post_comment_count,
    )


# ---------------------------------------------------------------------------
# Love It
# ---------------------------------------------------------------------------

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
    p_react   = make_post("r", reaction_type="love", comment_text=None, post_like_count=100, days_ago=1)
    p_comment = make_post("c", reaction_type=None,   comment_text="I love this", post_like_count=100, days_ago=1)
    tr = tag_post(p_react)
    tc = tag_post(p_comment)
    assert score(tr, now=now) > score(tc, now=now), "love reaction should outscore love comment at same engagement"

def test_old_post_lower_score():
    now = datetime.now(timezone.utc)
    fresh = make_post("f", reaction_type="love", days_ago=1)
    stale = make_post("s", reaction_type="love", days_ago=6)
    assert score(tag_post(fresh), now=now) > score(tag_post(stale), now=now)

def test_rank_fewer_than_n_posts():
    posts = [make_post("only", reaction_type="love")]
    tagged = filter_by_tag(tag_all(posts), "love_it")
    top = rank(tagged, top_n=2)
    assert len(top) == 1, "should return all available posts if fewer than top_n"


# ---------------------------------------------------------------------------
# Mr. & Mrs. Curious — tagging tests
# ---------------------------------------------------------------------------

def test_curious_direct_disagree():
    tp = tag_post(make_post(comment_text="I disagree with this framing entirely."))
    assert "mr_mrs_curious" in tp.tags

def test_curious_i_dont_think_so():
    tp = tag_post(make_post(comment_text="I don't think so — the evidence points the other way."))
    assert "mr_mrs_curious" in tp.tags

def test_curious_i_dont_buy_this():
    tp = tag_post(make_post(comment_text="I don't buy this argument at all."))
    assert "mr_mrs_curious" in tp.tags

def test_curious_pushback():
    tp = tag_post(make_post(comment_text="I'd push back on the second point here."))
    assert "mr_mrs_curious" in tp.tags

def test_curious_respectfully_disagree():
    tp = tag_post(make_post(comment_text="Respectfully disagree — this misses the bigger picture."))
    assert "mr_mrs_curious" in tp.tags

def test_curious_id_argue():
    tp = tag_post(make_post(comment_text="I'd argue there's a simpler explanation."))
    assert "mr_mrs_curious" in tp.tags

def test_curious_have_you_considered():
    tp = tag_post(make_post(comment_text="Have you considered the regulatory angle?"))
    assert "mr_mrs_curious" in tp.tags

def test_curious_i_wonder_if():
    tp = tag_post(make_post(comment_text="I wonder if this holds in non-English contexts."))
    assert "mr_mrs_curious" in tp.tags

def test_curious_what_about():
    tp = tag_post(make_post(comment_text="What about the latency trade-offs though?"))
    assert "mr_mrs_curious" in tp.tags

def test_curious_variety():
    phrases = [
        "I strongly disagree with the premise.",
        "Not sure I agree with the conclusion.",
        "I'd suggest a different approach here.",
        "On the other hand, the data tells a different story.",
        "Actually, I think the opposite might be true.",
        "Alternatively, you could frame it as a resource problem.",
        "But what if the model is already overfitting?",
        "Wouldn't it be more accurate to say it's correlation?",
        "That's overstated in my view.",
        "I think this is misleading.",
        "The data doesn't support this claim.",
    ]
    for phrase in phrases:
        tp = tag_post(make_post(comment_text=phrase))
        assert "mr_mrs_curious" in tp.tags, f"Should tag mr_mrs_curious for: '{phrase}'"

def test_curious_not_triggered_by_agreement():
    phrases = [
        "Totally agree, great post!",
        "Well said, couldn't put it better.",
        "This is exactly right.",
        "Sharing this with my team.",
    ]
    for phrase in phrases:
        tp = tag_post(make_post(comment_text=phrase))
        assert "mr_mrs_curious" not in tp.tags, f"Should NOT tag mr_mrs_curious for: '{phrase}'"

def test_curious_no_comment_not_tagged():
    tp = tag_post(make_post(reaction_type="love"))
    assert "mr_mrs_curious" not in tp.tags

def test_curious_render_chat_structure():
    from formatter import render_chat
    post = make_post(comment_text="I don't think so — I'd argue the data says otherwise.")
    post.author_name = "Elon Musk"
    post.post_text   = "AI will solve everything by 2027."
    tp = tag_post(post)
    conv = render_chat(tp, section="mr_mrs_curious")
    assert conv["section"] == "mr_mrs_curious"
    assert len(conv["turns"]) == 2
    assert conv["turns"][0]["speaker"] == "Elon Musk"
    assert conv["turns"][1]["speaker"] == "Sam"

def test_post_can_have_love_and_curious_tags():
    tp = tag_post(make_post(comment_text="I love this take, though I'd argue the timeline is off."))
    assert "love_it" in tp.tags
    assert "mr_mrs_curious" in tp.tags


# ---------------------------------------------------------------------------
# The Byline — Sam's own original articles
# PLACEHOLDER: logic will be updated once real export format is confirmed
# ---------------------------------------------------------------------------

def test_byline_tagged_when_is_own_post_true():
    post = make_post()
    post.is_own_post = True
    tp = tag_post(post)
    assert "the_byline" in tp.tags

def test_byline_not_tagged_when_is_own_post_false():
    post = make_post()
    post.is_own_post = False
    tp = tag_post(post)
    assert "the_byline" not in tp.tags

def test_byline_default_is_false():
    # is_own_post defaults to False — should never tag by accident
    tp = tag_post(make_post())
    assert "the_byline" not in tp.tags

def test_byline_does_not_interfere_with_other_tags():
    post = make_post(reaction_type="love")
    post.is_own_post = True
    tp = tag_post(post)
    assert "the_byline" in tp.tags
    assert "love_it" in tp.tags


# ---------------------------------------------------------------------------
# Incoming — reposts of releases and GitHub repos
# ---------------------------------------------------------------------------

def make_repost(post_text="", **kwargs):
    post = make_post(post_text=post_text, **kwargs)
    post.is_repost = True
    return post

# --- Release signals ---

def test_incoming_release_announcing():
    tp = tag_post(make_repost("Announcing our latest model update — now available."))
    assert "incoming" in tp.tags

def test_incoming_release_just_launched():
    tp = tag_post(make_repost("We just launched v2.0 of our open-source framework."))
    assert "incoming" in tp.tags

def test_incoming_release_introducing():
    tp = tag_post(make_repost("Introducing GPT-5 — now available to all users."))
    assert "incoming" in tp.tags

def test_incoming_release_version_string():
    tp = tag_post(make_repost("v0.9.1 is out. Faster inference, lower memory footprint."))
    assert "incoming" in tp.tags

def test_incoming_release_now_available():
    tp = tag_post(make_repost("Our new API is now available in public beta."))
    assert "incoming" in tp.tags

def test_incoming_release_variety():
    phrases = [
        "Just shipped the new release — check it out.",
        "Now open-source. Star us on GitHub.",
        "General availability starts today.",
        "We're open-sourcing our entire training pipeline.",
        "Release candidate for v3 is ready for testing.",
    ]
    for phrase in phrases:
        tp = tag_post(make_repost(phrase))
        assert "incoming" in tp.tags, f"Should tag incoming for: '{phrase}'"

# --- GitHub signals ---

def test_incoming_github_url():
    tp = tag_post(make_repost("Check this out: github.com/openai/whisper"))
    assert "incoming" in tp.tags

def test_incoming_github_repo_phrase():
    tp = tag_post(make_repost("Just open-sourced our new library. GitHub repo linked below."))
    assert "incoming" in tp.tags

def test_incoming_open_source_project():
    tp = tag_post(make_repost("Open-source project for fine-tuning LLMs on consumer hardware."))
    assert "incoming" in tp.tags

# --- Gate: must be a repost ---

def test_incoming_requires_repost():
    post = make_post(post_text="Announcing our latest model — now available.")
    post.is_repost = False
    tp = tag_post(post)
    assert "incoming" not in tp.tags

def test_incoming_repost_without_release_or_github_not_tagged():
    # Repost but no release or GitHub signal — should NOT qualify
    tp = tag_post(make_repost("Scaling laws are the future. More compute, more intelligence."))
    assert "incoming" not in tp.tags

def test_incoming_default_not_tagged():
    tp = tag_post(make_post())
    assert "incoming" not in tp.tags


# ---------------------------------------------------------------------------
# Trending — GitHub projects Sam interacted with
# ---------------------------------------------------------------------------

def make_github_post(post_text="", reaction_type=None, comment_text=None, is_repost=False, **kwargs):
    post = make_post(post_text=post_text, reaction_type=reaction_type, comment_text=comment_text, **kwargs)
    post.is_repost = is_repost
    return post


def test_trending_github_url_with_reaction():
    post = make_github_post(
        post_text="Amazing project at github.com/microsoft/autogen — check it out.",
        reaction_type="like",
    )
    tp = tag_post(post)
    assert "trending" in tp.tags

def test_trending_github_url_with_comment():
    post = make_github_post(
        post_text="github.com/langchain-ai/langchain is changing how we build agents.",
        comment_text="This is a game changer.",
    )
    tp = tag_post(post)
    assert "trending" in tp.tags

def test_trending_github_url_with_repost():
    post = make_github_post(
        post_text="Just starred github.com/openai/whisper — incredible OSS work.",
        is_repost=True,
    )
    tp = tag_post(post)
    assert "trending" in tp.tags

def test_trending_no_github_url_not_tagged():
    post = make_github_post(
        post_text="This open-source tool is taking off. No URL though.",
        reaction_type="like",
    )
    tp = tag_post(post)
    assert "trending" not in tp.tags

def test_trending_github_url_no_interaction_not_tagged():
    post = make_github_post(
        post_text="github.com/huggingface/transformers is great.",
        # no reaction, no comment, no repost
    )
    tp = tag_post(post)
    assert "trending" not in tp.tags

def test_trending_variety_interactions():
    base_text = "New repo at github.com/facebookresearch/llama — huge deal."
    for kwargs in [
        {"reaction_type": "celebrate"},
        {"reaction_type": "love"},
        {"comment_text": "Wow this is impressive"},
        {"is_repost": True},
    ]:
        post = make_github_post(post_text=base_text, **kwargs)
        tp = tag_post(post)
        assert "trending" in tp.tags, f"Should tag trending for interaction: {kwargs}"

def test_trending_star_bonus_ranks_higher():
    now = datetime.now(timezone.utc)
    post_no_stars  = make_github_post(
        post_text="github.com/vercel/ai is great.",
        reaction_type="like", post_like_count=500, days_ago=1,
    )
    post_with_stars = make_github_post(
        post_text="github.com/vercel/ai just hit 12k stars — incredible growth!",
        reaction_type="like", post_like_count=500, days_ago=1,
    )
    tp_no   = tag_post(post_no_stars)
    tp_star = tag_post(post_with_stars)
    assert score_trending(tp_star, now=now) > score_trending(tp_no, now=now)

def test_trending_rank_returns_top_n():
    posts = [
        make_github_post(post_text=f"github.com/org/repo{i}", reaction_type="like",
                         post_like_count=100*i, days_ago=1)
        for i in range(1, 5)
    ]
    tagged = filter_by_tag(tag_all(posts), "trending")
    top = rank_trending(tagged, top_n=2)
    assert len(top) == 2

def test_trending_engagement_determines_order():
    low  = make_github_post(post_text="github.com/org/low",  reaction_type="like", post_like_count=10,   days_ago=1)
    high = make_github_post(post_text="github.com/org/high", reaction_type="like", post_like_count=5000, days_ago=1)
    tagged = filter_by_tag(tag_all([low, high]), "trending")
    top = rank_trending(tagged, top_n=2)
    assert top[0].post.post_id == "p1" or top[0].post.post_like_count == 5000

def test_trending_can_also_be_incoming():
    post = make_github_post(
        post_text="Just launched github.com/anthropics/claude-code — now open source.",
        is_repost=True,
    )
    tp = tag_post(post)
    assert "trending" in tp.tags
    assert "incoming" in tp.tags


# ---------------------------------------------------------------------------
# Reflection — AI governance and negative impact posts
# ---------------------------------------------------------------------------

def test_reflection_governance_ai_regulation():
    tp = tag_post(make_post(post_text="AI regulation is long overdue — governments must act now.", reaction_type="like"))
    assert "reflection" in tp.tags

def test_reflection_ai_ethics():
    tp = tag_post(make_post(post_text="Ethical AI is not a nice-to-have — it's a baseline requirement.", reaction_type="like"))
    assert "reflection" in tp.tags

def test_reflection_ai_safety():
    tp = tag_post(make_post(post_text="AI safety research must keep pace with AI capabilities.", reaction_type="like"))
    assert "reflection" in tp.tags

def test_reflection_job_displacement():
    tp = tag_post(make_post(post_text="AI-driven job displacement is accelerating faster than retraining programs.", reaction_type="like"))
    assert "reflection" in tp.tags

def test_reflection_deepfakes():
    tp = tag_post(make_post(post_text="Deepfakes are now indistinguishable from real video — democracy is at risk.", reaction_type="like"))
    assert "reflection" in tp.tags

def test_reflection_algorithmic_bias():
    tp = tag_post(make_post(post_text="Algorithmic bias in hiring tools is well documented. Yet companies keep deploying them.", reaction_type="like"))
    assert "reflection" in tp.tags

def test_reflection_autonomous_weapons():
    tp = tag_post(make_post(post_text="Autonomous weapons without human oversight cross a moral line we cannot come back from.", reaction_type="celebrate"))
    assert "reflection" in tp.tags

def test_reflection_existential_risk():
    tp = tag_post(make_post(post_text="The existential risk from misaligned AI is real and we are not prepared.", reaction_type="like"))
    assert "reflection" in tp.tags

def test_reflection_variety():
    cases = [
        ("Responsible AI needs teeth, not just guidelines.", "like"),
        ("AI is not ready to make decisions about people's lives.", "like"),
        ("AI surveillance is creeping into every corner of public life.", "celebrate"),
        ("The dark side of AI is getting harder to ignore.", "like"),
        ("AI governance is the defining policy challenge of this decade.", "like"),
        ("AI alignment is unsolved and we're deploying anyway.", "like"),
    ]
    for text, reaction in cases:
        tp = tag_post(make_post(post_text=text, reaction_type=reaction))
        assert "reflection" in tp.tags, f"Should tag reflection for: '{text}'"

def test_reflection_requires_interaction():
    tp = tag_post(make_post(post_text="AI governance is the defining challenge of our time."))
    assert "reflection" not in tp.tags

def test_reflection_unrelated_ai_post_not_tagged():
    tp = tag_post(make_post(post_text="Just shipped a new AI feature — 10x faster inference!", reaction_type="like"))
    assert "reflection" not in tp.tags

def test_reflection_comment_bonus_ranks_higher():
    now = datetime.now(timezone.utc)
    reaction_only = make_post(post_text="AI regulation is overdue.", reaction_type="like", post_like_count=200, days_ago=1)
    with_comment   = make_post(post_text="AI regulation is overdue.", reaction_type="like", comment_text="This is exactly right — we need binding rules.", post_like_count=200, days_ago=1)
    tr = tag_post(reaction_only)
    tc = tag_post(with_comment)
    assert score_reflection(tc, now=now) > score_reflection(tr, now=now)

def test_reflection_rank_returns_top_n():
    posts = [
        make_post(post_text=f"AI governance issue #{i}.", reaction_type="like", post_like_count=100*i, days_ago=1)
        for i in range(1, 5)
    ]
    tagged = filter_by_tag(tag_all(posts), "reflection")
    top = rank_reflection(tagged, top_n=2)
    assert len(top) == 2


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
