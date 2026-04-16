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
from ranker import rank


def build_love_it_section(data_path: Path, top_n: int = 2) -> list[dict]:
    posts = load(data_path)
    tagged = tag_all(posts)
    love_posts = filter_by_tag(tagged, "love_it")
    top = rank(love_posts, top_n=top_n)

    results = []
    for tp in top:
        p = tp.post
        results.append({
            "section": "love_it",
            "score": tp.score,
            "author": p.author_name,
            "author_headline": p.author_headline,
            "post_url": p.post_url,
            "post_text": p.post_text[:300] + ("..." if len(p.post_text) > 300 else ""),
            "reaction": p.reaction_type,
            "comment": p.comment_text,
        })

    return results


def main():
    parser = argparse.ArgumentParser(description="Tech Digest Newsletter Builder")
    parser.add_argument("--data", required=True, help="Path to LinkedIn activity JSON")
    parser.add_argument("--top-n", type=int, default=2, help="Posts to include per section")
    args = parser.parse_args()

    love_it = build_love_it_section(Path(args.data), top_n=args.top_n)

    print("\n=== LOVE IT SECTION ===")
    for i, item in enumerate(love_it, 1):
        print(f"\n#{i} (score: {item['score']})")
        print(f"  Author:   {item['author']} — {item['author_headline']}")
        print(f"  URL:      {item['post_url']}")
        print(f"  Reaction: {item['reaction'] or '—'}")
        print(f"  Comment:  {item['comment'] or '—'}")
        print(f"  Preview:  {item['post_text'][:120]}...")


if __name__ == "__main__":
    main()
