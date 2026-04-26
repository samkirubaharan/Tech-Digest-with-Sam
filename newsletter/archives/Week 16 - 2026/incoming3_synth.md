## Incoming

Anthropic just made something quietly clever available on the Claude Platform: the **advisor-executor pattern** — and I think it's one of the more practical agent architecture ideas to land in a while.

Here's how it works:

- Pair **Claude Opus as an advisor** with Sonnet or Haiku as the executor
- When the executor hits a hard decision mid-task, it can consult Opus for a plan
- Opus responds, the executor picks back up — all within a **single API request**
- In evals, Sonnet + Opus advisor scored **2.7 points higher on SWE-bench Multilingual** than Sonnet alone
- Cost? **11.9% cheaper per task** than running Opus solo

**The big idea: you don't need Opus running the whole show — you just need it available at the right moments.**

This is how senior engineers actually work. You don't pull in your most expensive expert for every line of code — you call them when the decision actually matters. Anthropic is baking that pattern into the API itself.

The oracle is only as good as the question you know to ask — and deciding when to escalate will likely become its own engineering discipline.

---
*from [Sam Kirubaharan](https://www.linkedin.com/posts/sam-kirubaharan-5973b8110_were-bringing-the-advisor-strategy-to-the-activity-7448075792368037890-0uXc/?utm_source=share&utm_medium=member_desktop&rcm=ACoAABvS2EMBdcvEVlStK3KSLNS-UQaFKgd8BJ0) on LinkedIn*
