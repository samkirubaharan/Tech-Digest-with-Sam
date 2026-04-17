"""
Top-level orchestrator: loads data, tags it, produces newsletter sections.

Usage:
    python newsletter.py --data ../data/linkedin_activity.json
"""

import argparse
import json
from pathlib import Path

from loader import load
from tagger import tag_all, filter_by_tag
from ranker import rank, rank_trending, rank_reflection
from formatter import render_chat, print_chat


def main():
    parser = argparse.ArgumentParser(description="Tech Digest Newsletter Builder")
    parser.add_argument("--data", required=True, help="Path to LinkedIn activity JSON")
    parser.add_argument("--top-n", type=int, default=2, help="Posts to include per section")
    args = parser.parse_args()

    posts  = load(Path(args.data))
    tagged = tag_all(posts)

    # --- Love It ---
    love_posts = filter_by_tag(tagged, "love_it")
    top_love   = rank(love_posts, top_n=args.top_n)

    print("\n=== LOVE IT ===")
    for i, tp in enumerate(top_love, 1):
        p = tp.post
        print(f"\n#{i} (score: {tp.score})")
        print(f"  Author:   {p.author_name} — {p.author_headline}")
        print(f"  URL:      {p.post_url}")
        print(f"  Reaction: {p.reaction_type or '—'}")
        print(f"  Comment:  {p.comment_text or '—'}")
        print(f"  Preview:  {p.post_text[:120]}...")

    # --- Mr. & Mrs. Curious ---
    curious_posts = filter_by_tag(tagged, "mr_mrs_curious")
    top_curious   = rank(curious_posts, top_n=args.top_n)

    print("\n=== MR. & MRS. CURIOUS ===")
    for i, tp in enumerate(top_curious, 1):
        print(f"\n#{i} (score: {tp.score})")
        print_chat(render_chat(tp, section="mr_mrs_curious"))

    # --- The Byline ---
    byline_posts = filter_by_tag(tagged, "the_byline")
    top_byline   = rank(byline_posts, top_n=args.top_n)

    print("\n=== THE BYLINE ===")
    if not top_byline:
        print("\n  [placeholder — no own articles detected in this dataset]")
    for i, tp in enumerate(top_byline, 1):
        p = tp.post
        print(f"\n#{i} (score: {tp.score})")
        print(f"  URL:      {p.post_url}")
        print(f"  Preview:  {p.post_text[:200]}...")

    # --- Incoming ---
    incoming_posts = filter_by_tag(tagged, "incoming")
    top_incoming   = rank(incoming_posts, top_n=args.top_n)

    print("\n=== INCOMING ===")
    if not top_incoming:
        print("\n  [no reposts of releases or GitHub repos found in this dataset]")
    for i, tp in enumerate(top_incoming, 1):
        p = tp.post
        print(f"\n#{i} (score: {tp.score})")
        print(f"  Author:   {p.author_name} — {p.author_headline}")
        print(f"  URL:      {p.post_url}")
        print(f"  Preview:  {p.post_text[:200]}...")

    # --- Trending ---
    trending_posts = filter_by_tag(tagged, "trending")
    top_trending   = rank_trending(trending_posts, top_n=args.top_n)

    print("\n=== TRENDING ===")
    if not top_trending:
        print("\n  [no trending GitHub projects found in this dataset]")
    for i, tp in enumerate(top_trending, 1):
        p = tp.post
        print(f"\n#{i} (score: {tp.score})")
        print(f"  Author:   {p.author_name} — {p.author_headline}")
        print(f"  URL:      {p.post_url}")
        print(f"  Preview:  {p.post_text[:200]}...")

    # --- Reflection ---
    reflection_posts = filter_by_tag(tagged, "reflection")
    top_reflection   = rank_reflection(reflection_posts, top_n=args.top_n)

    print("\n=== REFLECTION ===")
    if not top_reflection:
        print("\n  [no AI governance or impact posts found in this dataset]")
    for i, tp in enumerate(top_reflection, 1):
        p = tp.post
        print(f"\n#{i} (score: {tp.score})")
        print(f"  Author:   {p.author_name} — {p.author_headline}")
        print(f"  URL:      {p.post_url}")
        print(f"  Comment:  {p.comment_text or '—'}")
        print(f"  Preview:  {p.post_text[:200]}...")


if __name__ == "__main__":
    main()
