"""
Renders tagged posts into display-ready formats for each newsletter section.
"""

from models import TaggedPost

SAM = "Sam"


def render_chat(tagged_post: TaggedPost, section: str = "mr_mrs_curious") -> dict:
    """
    Render a conversation-based post as a two-turn chat exchange.
    Used for Mr. & Mrs. Curious and any other conversation-based sections.

    Returns a dict with:
      - section       : section tag
      - author        : author name
      - author_headline
      - post_url
      - turns         : list of {"speaker": str, "text": str}
    """
    p = tagged_post.post
    turns = [
        {"speaker": p.author_name, "text": p.post_text},
        {"speaker": SAM,           "text": p.comment_text or ""},
    ]
    return {
        "section": section,
        "author": p.author_name,
        "author_headline": p.author_headline,
        "post_url": p.post_url,
        "turns": turns,
    }


def print_chat(conversation: dict) -> None:
    """Pretty-print a conversation section entry to stdout."""
    print(f"  {conversation['author']}  ({conversation['author_headline']})")
    print(f"  {conversation['post_url']}\n")
    for turn in conversation["turns"]:
        label = f"  {turn['speaker']}".ljust(20)
        text  = turn["text"][:280] + ("..." if len(turn["text"]) > 280 else "")
        print(f"{label}  \"{text}\"")
        print()
