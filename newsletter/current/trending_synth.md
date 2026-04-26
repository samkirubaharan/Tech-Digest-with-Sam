## Trending

### The AMD Engineer Who Proved Claude Code Got Worse

This one matters — not just as a story about model quality, but as a story about trust in AI tooling.

Stella Laurenzo, Senior Director of AI at AMD, had been running Claude Code across 50+ concurrent agent sessions for serious systems work — C, MLIR, GPU drivers. Around February, things started feeling different. Not broken. Shallower. So she pulled the logs.

**6,852 session files. 17,871 thinking blocks. 234,760 tool calls.** She ran a regression analysis precise enough to name the exact date the performance cliff appeared.

The findings are hard to argue with:

- **Thinking depth collapsed from 2,200 to 720 characters** — a 67% drop — then fell further to 600 once thinking redaction rolled out fully by March 12
- **The Read:Edit ratio dropped from 6.6 to 2.0** — a third of file edits were now happening on files the model had never read
- **Monthly API costs went from $345 to $42,000** — the same workload, 64x more tokens, demonstrably worse output. AMD switched providers.

But the most damning detail: **thinking depth dropped in late February, before the thinking redaction feature rolled out on March 8.** Anthropic's public narrative was that they were hiding thinking summaries for speed — but the behavioral deterioration started weeks earlier, when thinking was still fully visible.

Anthropic confirmed two changes. On February 9th, Opus 4.6 introduced adaptive thinking. On March 3rd, the default effort level was quietly reduced from high to medium. The first change was announced. The second wasn't.

This is a strong argument for putting LLM tooling through a CI pipeline. When code still behaves the same way on the surface but the model's reasoning has quietly degraded, you won't know unless you measure it.

---
*from [Sam Kirubaharan](https://www.linkedin.com/posts/sam-kirubaharan-5973b8110_a-compelling-reason-for-putting-llm-software-share-7452814467668647936-X2xb/) on LinkedIn*
