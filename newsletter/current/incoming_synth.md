## Incoming

### Kiro CLI 2.0: Headless, Windows-Native, and Generally Available

AWS VP Swami Sivasubramanian announced Kiro CLI 2.0 this week — a meaningful step up from the experimental release, built specifically for developers who live in the terminal.

Here's what changed:

- **Headless mode** — Kiro CLI can now run programmatically inside CI/CD pipelines. Trigger it to troubleshoot production failures, generate pull requests, or run long-standing prompts without a human at the keyboard. This is the feature that makes Kiro useful in automated workflows, not just interactive development sessions
- **Windows support** — native. Not a workaround, not WSL. If you're on Windows, you're no longer second-class in the Kiro ecosystem
- **UX refresh is now fully GA** — the new experience exits experimental mode and becomes the default. It includes a new subagent architecture and a task list so you can track what the agent is actually doing at any point in the session

The headless CI/CD integration is the one worth paying attention to. Agentic CLI tools that only work interactively are bounded by human availability. Headless mode is what shifts a tool from "developer assistant" to "autonomous pipeline component" — you point your CI at it, define the prompt, and it executes as part of your build or deploy process.

AWS entering this space seriously means the agentic CLI market is no longer just Anthropic's territory.

---
*from [Swami Sivasubramanian](https://www.linkedin.com/posts/swaminathansivasubramanian_kiro-cli-20-is-here-with-a-new-look-and-ugcPost-7450379013510062080-c_JQ/) on LinkedIn*
