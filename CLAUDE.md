# Tech Digest with Sam — Agent Instructions

## Overview

This repo is the production pipeline for the weekly LinkedIn newsletter "Tech Digest with Sam". Each week follows this flow:

1. Sam saves LinkedIn posts as `.mhtml` files, named by category (e.g. `Byline1.mhtml`, `Trending2.mhtml`)
2. Files are placed in `newsletter/current/` alongside `front_cover.md` and `back_cover.md`
3. The agent synthesises each file into a `*_synth.md` article and updates `front_cover.md` with the TOC
4. Outputs are rendered, archived, and pushed

## Tagging Is Always Pre-Provided

Sam always names the mhtml files by section (Byline, Trending, LoveIt, Incoming, MrMsCurious, Reflect). **Skip the tagging step entirely.** Do not run `tagger.py`, `ranker.py`, or any classification logic. Use the file name as the ground truth section assignment.

Section name → newsletter heading mapping:
| File prefix | Section heading |
|---|---|
| `Byline` | Byline |
| `Trending` | Trending |
| `LoveIt` | Love It! |
| `Incoming` | Incoming |
| `MrMsCurious` | Mr & Ms Curious |
| `Reflect` | Reflect |

## Synthesis — How to Write Each _synth.md

Read the source mhtml file. Extract the post text and URL. Write a newsletter article in Sam's voice.

**Voice:** Direct, first-person where appropriate, opinionated but grounded. No fluff. Written for a technical LinkedIn audience that values signal over hype.

**Format per file:**
```
## <Section Heading>

[article body — 200–400 words, bullet points where relevant]

---
*from [Author Name](url) on LinkedIn*
```

**Mr & Ms Curious** — always written as a two-voice dialogue between Mr. Curious and Ms. Curious. One takes a position, the other challenges it. Sam's actual view should be inferable from the exchange but never stated directly.

**Byline** — first-person Sam. These are his own posts/articles. Expand the ideas, don't just summarise.

**Trending** — third-person or analytical. What's the story, why does it matter, what's the implication.

**Love It!** — what it is, what makes it worth loving, one concrete observation or use case.

**Incoming** — news digest style. What dropped, what it means collectively.

**Reflect** — more personal/philosophical. Slower pace. Ends with an open thought.

## File Layout

```
newsletter/
  current/           ← active week's source and output files
    front_cover.md
    back_cover.md
    *_synth.md        ← generated articles (one per mhtml)
  archives/
    Week <N> - <Year>/  ← completed issues (mhtml moved to data/)
data/                ← source mhtml files for the current week
```

## front_cover.md

After all synth files are written, update `newsletter/current/front_cover.md`:
- Change the week number in the heading
- Fill the TOC table with one row per article: Genre | Title | Page (page = row order starting at 2)

## back_cover.md

Carry forward from the previous week unchanged, updating only the week number in `## Week N, Year` and the footer line.
