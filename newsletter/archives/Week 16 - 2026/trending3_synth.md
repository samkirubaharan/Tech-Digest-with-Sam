## Trending

### Agent Tool Design Is More Art Than Science

There's a piece out from Thariq Shihipar on the Anthropic/Claude blog that I keep thinking about: *Seeing Like an Agent: How We Design Tools in Claude Code.*

The core thesis is deceptively simple — designing the tools that an AI agent uses is one of the hardest problems in building agents, and there's no formula for getting it right.

A few things that stood out:

- **Tool design is fundamentally iterative** — the Claude Code team didn't architect the perfect toolset upfront; they discovered it through cycles of building, observing, and adjusting
- The agent needs to "see" the world through its tools, which means poorly scoped tools don't just limit capability — they actively distort how the agent reasons
- Intuition plays a huge role; it's more like UX design than systems engineering

What strikes me is how this challenges the way most teams approach agent development. We spend a lot of time on model selection, prompt engineering, memory architecture — but the tooling layer often gets treated as an afterthought.

**If the tools are the agent's senses, then bad tools don't just slow it down — they make it blind in ways it can't even detect.**

Worth a read if you're building anything with agents. The full post is at claude.com/blog/seeing-like-an-agent.

Most teams are still bolting on capabilities as they go. The ones treating tool design as a first-class discipline will build significantly better agents.

---
*from [Sam Kirubaharan](https://www.linkedin.com/posts/sam-kirubaharan-5973b8110_seeing-like-an-agent-how-we-design-tools-activity-7448554624321732608-Bx7O/?utm_source=share&utm_medium=member_desktop&rcm=ACoAABvS2EMBdcvEVlStK3KSLNS-UQaFKgd8BJ0) on LinkedIn*
