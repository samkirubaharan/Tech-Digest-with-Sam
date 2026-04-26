## Love It!

There's a context management problem in Claude Code that most people don't notice until it's already bitten them: you're mid-task, you have a quick question, you ask it in the main thread — and now that question, its answer, and Claude's recalibration around it are sitting in your context for the rest of the session.

Alice Zhao surfaced the fix this week: **`/btw`** (or `Cmd+` on desktop).

It opens an instant side chat. Ask your one-off question. Close it. The main thread is untouched.

I've been using `/btw` on CLI for a while, but tried the Desktop App version last week — it opens a small floating window and tracks all your `/btw` requests separately. The interface makes it feel even more intentional: this is a different stream, and you know it.

The underlying principle is worth internalising. On long agentic runs, a single "quick question" in the main thread can quietly distort the next 50 turns. Claude adjusts its model of what you're doing based on everything in context — including the tangents. `/btw` is a context discipline tool as much as a convenience feature.

It's one of those features that seems minor until you start using it consistently. Then you notice how often you were polluting your own sessions.

---
*from [Alice Zhao](https://www.linkedin.com/posts/alicezhao1991_claude-code-on-desktop-tip-most-people-ugcPost-7452415293143797760-DuLK/) on LinkedIn*
