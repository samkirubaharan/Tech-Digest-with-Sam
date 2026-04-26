## Byline

The Opus 4.7 launch generated a lot of benchmark noise. I had two observations that I think cut deeper than the headline numbers.

**Why software is the domain AI is actually solving**

It's not accidental that LLMs feel so capable in software and so unreliable almost everywhere else. Andrej Karpathy framed this with what he called the "car wash question" — the gap between how software people and non-software people perceive LLM success.

The answer is validation schemes. Software has them built in: unit tests, UI tests, spec validators, binary pass/fail signals. Most real-world problems don't have anything like that. There's no equivalent of `npm test` for "did this business decision work out." LLMs haven't "solved" those domains because there's no feedback signal to iterate against.

The practical takeaway: before you hand a problem to an LLM, invest time defining your validation metric. Once you have one, you can let the model iterate until completion. Without it, you're just hoping.

**The Pareto cost buried in the benchmark chart**

Opus 4.7 consistently improves performance across effort levels without consuming extra tokens — with one exception. That final jump from 71 to 75 on the benchmark costs 2× the tokens: 120K to 220K. A 4-point gain for double the compute.

That's Pareto's Principle hiding in the chart. 80% of the result for 20% of the effort, and then a cliff where the last few percentage points become extremely expensive to chase.

This matters practically. In most real cases, 80% is the real finish line. The last 4% is worth something — but it's worth deliberately deciding whether you need it before you pay for it.

Perfection is expensive. Give that calculation genuine thought before you chase it.

---
*from [Sam Kirubaharan](https://www.linkedin.com/posts/sam-kirubaharan-5973b8110_ai-claudeopus-llm-ugcPost-7451640761986580480-0K1m/) on LinkedIn*
