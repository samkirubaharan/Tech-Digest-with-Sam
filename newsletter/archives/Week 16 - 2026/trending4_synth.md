## Trending

### LangWatch Red-teaming

The LangWatch team just open-sourced an automated red-teaming tool for AI agents — announced by Manouk Draisma — and it addresses something most teams are quietly ignoring.

The post opens with a sharp observation: turn on the news and AI sounds terrifying — deepfakes, voice cloning, disinformation, data authorities calling agents "Trojan horses." Those concerns are real. But the harder and more immediate question is whether the AI systems we're building can actually hold up under deliberate attack.

The specific problem: attacks on AI agents don't look like one hostile prompt. They look like a patient, escalating conversation — building trust over multiple turns, probing edges quietly — until the agent gives up something it shouldn't. Most test suites aren't built for this. They're built for happy paths and obvious failures.

That's the gap **LangWatch Red-teaming** is designed to close:

- **Multi-turn attack simulation** — models the slow crescendo of a real adversarial conversation, not just isolated edge cases
- **Crescendo escalation** — a specific technique that mirrors how real-world manipulation unfolds over time, gradually pushing the agent past its guardrails
- **Automated adversarial testing at scale** — not manual edge case writing, but systematic pressure across the attack surface
- **CI/CD integration** — plugs into your pipeline so safety testing is continuous, not a one-time pre-launch audit
- One method call to get started

The gap between "passes all our tests" and "safe in production" is real, and most teams are not closing it. Testing agentic systems at the unit or integration level is something the industry is still largely winging.

This is open source and part of LangWatch Scenario. If you're building anything with AI agents that touches customer data, internal systems, or complex workflows — this is a serious place to start.

---
*from [Manouk Draisma](https://www.linkedin.com/posts/manoukdraisma_exciting-announcement-below-turn-on-activity-7449770511988985856-6Qxc/?utm_source=share&utm_medium=member_desktop&rcm=ACoAABvS2EMBdcvEVlStK3KSLNS-UQaFKgd8BJ0) on LinkedIn*
