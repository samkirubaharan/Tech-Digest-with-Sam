## Byline

Claude Code is a genuinely different tool depending on how you handle the session — and I've been underusing some of its most useful commands.

The Claude Code team recently published a session management guide, and a few commands in there deserve more visibility than they're getting.

Here's the rundown that I shared this week:

- **`/usage`** — shows your usage plan limits and rate limits. Already a button in the Claude Desktop app (look for the pie icon at the footer). On CLI, you'll want to set up a status line instead — Claude itself will walk you through it
- **`/rewind`** — resets the conversation to a previous checkpoint. This is the preferred way to course-correct. When you disagree with where Claude went, don't just keep prompting around it — rewind and remove the conflicting trace from context entirely
- **`/clear`** — wipes context to a fresh slate. Use when you're genuinely starting a new task and don't want the noise from the previous one bleeding in
- **`/compact`** — compresses context into concise summaries. Useful inside long sessions, or when you want to hand information across steps without a full context reset

The one I keep coming back to is `/rewind`. There's a real failure mode where you disagree with Claude, say so, Claude "adjusts" — but the original misguided reasoning is still sitting in context, quietly influencing everything downstream. Rewind removes that. It forks the conversation at a clean point.

And you have three options when rewinding: fully ignore the direction taken (clean fork), or summarise everything that happened after the restore point so Claude carries the learning without carrying the wrong path. That second option is underrated.

The `/usage` status line detail is worth acting on too. If you're on CLI and want live usage visibility without leaving the terminal, just ask Claude to set it up. It handles the configuration itself.

---
*from [Sam Kirubaharan](https://www.linkedin.com/posts/sam-kirubaharan-5973b8110_claudecode-sessionmanagent-claudeblog-share-7452033807928492032-AKra/) on LinkedIn*
