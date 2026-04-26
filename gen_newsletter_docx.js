const {
  Document, Packer, Paragraph, TextRun, AlignmentType,
  HeadingLevel, LevelFormat, ExternalHyperlink, BorderStyle
} = require('docx');
const fs = require('fs');

// ── helpers ──────────────────────────────────────────────────────────────────

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun({ text, bold: true, size: 36, font: 'Calibri' })],
    spacing: { before: 360, after: 120 },
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    children: [new TextRun({ text, bold: true, size: 28, font: 'Calibri' })],
    spacing: { before: 280, after: 80 },
  });
}

function sectionLabel(label) {
  return new Paragraph({
    children: [new TextRun({ text: `【 ${label} 】`, bold: true, size: 22, color: '2E75B6', font: 'Calibri' })],
    spacing: { before: 400, after: 80 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: '2E75B6', space: 4 } },
  });
}

// Parse inline **bold** and *italic* into TextRun array
function parseRuns(text, baseSize = 22) {
  const runs = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*)/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) runs.push(new TextRun({ text: text.slice(last, m.index), size: baseSize, font: 'Calibri' }));
    const inner = m[0];
    if (inner.startsWith('**')) {
      runs.push(new TextRun({ text: inner.slice(2, -2), bold: true, size: baseSize, font: 'Calibri' }));
    } else {
      runs.push(new TextRun({ text: inner.slice(1, -1), italics: true, size: baseSize, font: 'Calibri' }));
    }
    last = m.index + m[0].length;
  }
  if (last < text.length) runs.push(new TextRun({ text: text.slice(last), size: baseSize, font: 'Calibri' }));
  return runs;
}

function p(text) {
  return new Paragraph({
    children: parseRuns(text),
    spacing: { before: 80, after: 80 },
  });
}

function italic(text) {
  return new Paragraph({
    children: [new TextRun({ text, italics: true, size: 20, color: '595959', font: 'Calibri' })],
    spacing: { before: 60, after: 60 },
  });
}

function bullet(text) {
  return new Paragraph({
    numbering: { reference: 'bullets', level: 0 },
    children: parseRuns(text),
    spacing: { before: 40, after: 40 },
  });
}

function quote(speaker, text) {
  return new Paragraph({
    children: [
      new TextRun({ text: `${speaker}: `, bold: true, size: 22, font: 'Calibri', color: '2E75B6' }),
      new TextRun({ text, italics: true, size: 22, font: 'Calibri' }),
    ],
    spacing: { before: 60, after: 60 },
    indent: { left: 720 },
  });
}

function divider() {
  return new Paragraph({
    children: [new TextRun({ text: '\u2500 \u2500 \u2500 \u2500 \u2500 \u2500 \u2500 \u2500 \u2500 \u2500 \u2500 \u2500 \u2500 \u2500 \u2500 \u2500 \u2500 \u2500 \u2500 \u2500', size: 18, color: 'CCCCCC', font: 'Calibri' })],
    spacing: { before: 200, after: 200 },
    alignment: AlignmentType.CENTER,
  });
}

function source(author, url) {
  return new Paragraph({
    children: [
      new TextRun({ text: 'from ', italics: true, size: 20, color: '595959', font: 'Calibri' }),
      new ExternalHyperlink({
        link: url,
        children: [new TextRun({ text: author, italics: true, size: 20, color: '2E75B6', underline: {}, font: 'Calibri' })],
      }),
      new TextRun({ text: ' on LinkedIn', italics: true, size: 20, color: '595959', font: 'Calibri' }),
    ],
    spacing: { before: 100, after: 60 },
  });
}

function blank() {
  return new Paragraph({ children: [new TextRun('')], spacing: { before: 40, after: 40 } });
}

// ── document ─────────────────────────────────────────────────────────────────

const doc = new Document({
  numbering: {
    config: [
      {
        reference: 'bullets',
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: '\u2022', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } },
        }],
      },
    ],
  },
  styles: {
    default: { document: { run: { font: 'Calibri', size: 22 } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 36, bold: true, font: 'Calibri', color: '1F3864' },
        paragraph: { spacing: { before: 360, after: 120 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 28, bold: true, font: 'Calibri', color: '2E75B6' },
        paragraph: { spacing: { before: 280, after: 80 }, outlineLevel: 1 } },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
      },
    },
    children: [

      // ── HEADER ──────────────────────────────────────────────────────────────
      h1('Tech Digest with Sam'),
      new Paragraph({
        children: [new TextRun({ text: 'Week 16, 2026', size: 24, color: '595959', font: 'Calibri' })],
        spacing: { before: 0, after: 40 },
      }),
      new Paragraph({
        children: [new TextRun({ text: 'Tech Digest with Sam brings you the latest news on Tech & AI.', size: 22, italics: true, color: '595959', font: 'Calibri' })],
        spacing: { before: 0, after: 200 },
      }),
      divider(),

      // ── BYLINE 1 — Harness Engineering ──────────────────────────────────────
      sectionLabel('Byline'),
      h2('Harness Engineering: The New Frontier of Agentic Design'),
      p("There\u2019s a framing I\u2019ve been sitting with lately that I think cuts closer to the truth about where AI engineering is heading than most takes out there: **the real frontier isn\u2019t writing better LLM prompts \u2014 it\u2019s designing the harness around the model.**"),
      blank(),
      p("I published a piece on this recently, and the core idea is that Agentic Harnessing is genuinely hard in a way that software engineering is quickly ceasing to be. LLMs are already close to \u201csolved\u201d for verifiable tasks \u2014 give them a spec and a test suite and they\u2019ll iterate toward it. But building the environment in which an agent reliably operates? That\u2019s still a deeply human problem, and it\u2019s one that AI can\u2019t yet bootstrap itself out of."),
      blank(),
      p("Here\u2019s what Harness Engineering actually involves:"),
      bullet("**Context Engineering** \u2014 deciding what information the agent sees and when, so it stays sharp and doesn\u2019t get polluted by noise"),
      bullet("**Feedback Loops** \u2014 feeding activity back to the agent to compound knowledge and prevent the same mistakes repeating"),
      bullet("**Advanced Tooling** \u2014 targeted scripts and MCPs that introduce determinism into an inherently non-deterministic model"),
      bullet("**Structured Paths** \u2014 defining explicit state transitions so an agent moves with intent instead of wandering"),
      blank(),
      italic("\u201cThe harness is what bridges the gap between a raw model and a sophisticated, reliable digital employee.\u201d"),
      blank(),
      p("Software engineers are starting to feel like the hard part of their job is disappearing. What\u2019s emerging in its place is this discipline \u2014 part architect, part systems thinker \u2014 that I\u2019m calling the Harness Engineer. There\u2019s no universal test suite for whether a harness is \u201cgood.\u201d That judgment still requires human intuition \u2014 and right now, not many people are deliberately building it."),
      source('Sam Kirubaharan', 'https://www.linkedin.com/pulse/harness-engineering-new-frontier-agenticdesign-sam-kirubaharan-uoa2c/'),
      divider(),

      // ── TRENDING 1 — Opus 4.7 ───────────────────────────────────────────────
      sectionLabel('Trending'),
      h2('Anthropic Just Dropped Opus 4.7 \u2014 and It Verifies Its Own Work'),
      p("There\u2019s no \u201clater\u201d anymore at Anthropic. Claude Opus 4.7 landed this week, and if you\u2019ve been following the model race, this one has a few features worth actually paying attention to."),
      blank(),
      p("The headline isn\u2019t just benchmark scores. It\u2019s what\u2019s baked into the model itself:"),
      bullet("**Self-verification is now native** \u2014 Opus 4.7 checks its own outputs before reporting back, without you needing to prompt it to do so"),
      bullet("Agentic coding scores have jumped significantly \u2014 it\u2019s built for long-running tasks with less hand-holding"),
      bullet("Vision got a serious upgrade: 3x higher resolution, which means usable outputs for interfaces, slides, and docs"),
      bullet("Grounding techniques are now built into the model layer, not bolted on through tool calls"),
      bullet("Cybersecurity guardrails have been tightened (a miniature version of the Mythos framework)"),
      blank(),
      p("The verification step is the thing I keep coming back to. Anthropic made a deliberate architectural decision to bake it into the model rather than into Claude Code or another tool layer. That\u2019s meaningful \u2014 it means the behavior travels with the model across every deployment, not just the ones where someone remembered to add the check."),
      blank(),
      p("**That\u2019s the shift: from \u201cprompt it to verify\u201d to \u201cit just does.\u201d**"),
      blank(),
      p("The grounding bullet is worth pausing on too. Each major AI platform has its own approach here \u2014 Google grounds via Google Search, Amazon grounds via Specification. This is Anthropic\u2019s way: grounding built into the model layer itself, not as an external tool call or integration. Same destination, very different architectural choices."),
      blank(),
      p("An idea worth exploring: what if model verification capabilities were linked natively to business verification schemes? The model already checks its own outputs \u2014 imagine that wired directly into your compliance rules, approval workflows, or domain-specific quality gates. Native verification meets business logic, without the glue code in between."),
      source('Sam Kirubaharan', 'https://www.linkedin.com/feed/update/urn:li:activity:7449738988829159424/'),
      divider(),

      // ── LOVE IT 1 — Claude Design ────────────────────────────────────────────
      sectionLabel('Love It!'),
      h2('Claude Design Is Here \u2014 and I\u2019m Using It'),
      p("Anthropic just dropped Claude Design and I have to talk about it \u2014 this one genuinely surprised me."),
      blank(),
      p("A dedicated tool for creating designs, prototypes, slides, and one-pagers entirely through conversation. No drag-and-drop. No template browsing. Just describe what you want, and Claude builds the first version."),
      blank(),
      p("Here\u2019s what makes this more than a cool demo:"),
      bullet("**Powered by Claude Opus 4.7 Vision** \u2014 actually understands visual context, not just text prompts"),
      bullet("**Reads your codebase and design files** to build your team\u2019s design system automatically \u2014 every output stays on-brand without manual style enforcement"),
      bullet("Iterate through conversation, inline comments, direct edits, or custom sliders"),
      bullet("Export to Canva, PDF, or PPTX \u2014 or hand off directly to Claude Code for implementation"),
      bullet("Available now in research preview on Pro, Max, Team, and Enterprise plans"),
      blank(),
      p("The part I keep coming back to: it learns your design system from your actual files. That\u2019s the move that shifts this from novelty to real workflow change. Brand guidelines in a Figma file or CSS tokens? Claude internalises that and applies it consistently. Most design tools still can\u2019t do that."),
      blank(),
      p("We\u2019re watching the design handoff problem get quietly solved \u2014 and I absolutely love it."),
      blank(),
      p("Full disclosure: this newsletter is designed using Claude Design. I\u2019ve been using it personally and it\u2019s been a genuinely great experience. Try it at claude.ai/design."),
      source('Sam Kirubaharan', 'https://www.linkedin.com/posts/sam-kirubaharan-5973b8110_introducing-claude-design-by-anthropic-labs-activity-7450930200525115392-keiv/'),
      divider(),

      // ── REFLECT 2 — When AI Works Exactly as Designed ───────────────────────
      sectionLabel('Reflect'),
      h2('When AI Works Exactly as Designed'),
      p("The question we keep asking about AI is: *what happens when it goes wrong?*"),
      blank(),
      p("Lauren Good asks a harder one: **what happens when it goes exactly right?**"),
      blank(),
      p("In a white paper published this week, Lauren \u2014 Human Systems Architect and Licensed Clinical Consultant \u2014 examines two events that arrived just 13 days apart. A Los Angeles jury found Meta and Google liable for deliberately designing platforms to addict children. Days later, Anthropic disclosed it had withheld Claude Mythos Preview because of what it autonomously did to critical software infrastructure \u2014 while working as intended."),
      blank(),
      p("Neither system failed. Both reshaped the people inside them."),
      blank(),
      p("Lauren calls this the **Formation Effect** \u2014 what AI does to human judgment, competence, and autonomy during normal, correct, intended use. It operates through four dimensions:"),
      bullet("**Skill Foreclosure** \u2014 unaided competence quietly erodes through disuse, not failure"),
      bullet("**Behavioural Masking** \u2014 people adapt to what the system rewards, until the adaptation feels like identity"),
      bullet("**Oversight Fragility** \u2014 as trust in a system grows, human supervision thins \u2014 not through negligence, but through rational deference"),
      bullet("**Regenerative Agency** \u2014 can people still reach for self-direction, or has the system made that feel unnecessary?"),
      blank(),
      p("Current governance frameworks \u2014 the EU AI Act, voluntary safety evaluations, jailbreak testing \u2014 are all built to catch what goes wrong. None of them measure what goes right and still quietly reshapes the humans operating inside it."),
      blank(),
      p("The effect AI and software products can create on us when they work just as expected \u2014 that\u2019s the part we\u2019re not yet measuring."),
      source('Lauren Good', 'https://www.linkedin.com/posts/lauren-good-b031613b1_when-ai-works-exactly-as-designed-ugcPost-7450750162248949760-sXr6'),
      divider(),

      // ── INCOMING 1 — Three Drops ─────────────────────────────────────────────
      sectionLabel('Incoming'),
      h2("Anthropic\u2019s Three Drops and What They Signal"),
      p("Anthropic just dropped three things in close succession \u2014 and together they point at something bigger than any single release."),
      blank(),
      p("Here\u2019s what landed:"),
      bullet("**Claude Opus 4.7** \u2014 the new flagship model. Stronger agentic coding scores, built-in output verification before it reports back, 3x higher image resolution, and meaningfully better at following complex instructions"),
      bullet("**Claude Code Routines** \u2014 scheduled, API-triggered, and GitHub-triggered automation that spins up Claude Code Web instances autonomously. No machine needs to stay awake. No IDE required"),
      bullet("**Redesigned Claude desktop app** \u2014 rebuilt from the ground up for parallel work. Integrated terminal, in-app file editing, rebuilt diff viewer, side chats, SSH connections"),
      blank(),
      p("**The throughline: Anthropic isn\u2019t building a better chatbot. They\u2019re building a software development operating system.**"),
      blank(),
      p("Routines is the one I keep thinking about. The old Schedules feature required your machine to be running. Routines runs entirely via Claude Code Web \u2014 so you can trigger nightly issue triage, PR reviews, alert triage, or cross-repo SDK ports without any local infra. That\u2019s IDE-less development becoming genuinely viable, not just a talking point."),
      blank(),
      p("And Opus 4.7 verifying its own outputs before surfacing results? That\u2019s not a small tweak \u2014 it\u2019s Anthropic baking epistemic discipline into the model itself rather than leaving it to prompt engineering."),
      blank(),
      p("At some point \u201cAI coding assistant\u201d stops being an accurate frame. We\u2019re already past it."),
      source('Sam Kirubaharan', 'https://www.linkedin.com/feed/update/urn:li:activity:7450562449524625408/'),
      divider(),

      // ── BYLINE 3 — Knowledge That Compounds ─────────────────────────────────
      sectionLabel('Byline'),
      h2('Knowledge That Compounds'),
      p("Graphify is worth your attention \u2014 an extended version of Karpathy\u2019s knowledge workflow, now open source and runnable in a single command. Karpathy had been manually piping papers, tweets, and screenshots into an LLM-compiled wiki, navigated through Obsidian. Knowledge that compounds every time you add something new. His closing line: *\u201cI think there is room here for an incredible new product instead of a hacky collection of scripts.\u201d* Graphify shipped days later."),
      blank(),
      p("For real work though, I prefer building it bottom-up \u2014 starting from nothing and adding only the minimum required."),
      blank(),
      p("That\u2019s what my KB skill set does. Three skills, one loop:"),
      bullet("**KB Gather** \u2014 pulls from JIRA tickets, web pages, documents (Word, Excel, PowerPoint), codebase, and chat/call transcripts including LLM conversations \u2014 and writes everything into a folder of markdown files"),
      bullet("**KB Consult** \u2014 attaches relevant KB topics to an active chat session for Q&A and context enrichment. Detaches when you\u2019re done"),
      bullet("**KB Digest** \u2014 takes new things learned during a session and writes them back into the KB"),
      blank(),
      p("**The magic is in running it iteratively on the same data.** Each pass, the KB gets more accurate. Connections sharpen. Gaps fill in. The LLM indexes the knowledge and renders only what\u2019s relevant when it\u2019s needed \u2014 no bloat, no noise."),
      blank(),
      p("This is the core of what Karpathy was after: **knowledge that compounds.** Every ticket, every doc, every conversation makes the next one sharper."),
      blank(),
      p("Simple to build, lightweight to run \u2014 and surprisingly effective. The bigger frameworks have their place, but for a developer deep in daily work, this kind of minimal loop often does more than you\u2019d expect from something so lean."),
      source('Sam Kirubaharan', 'https://www.linkedin.com/posts/sam-kirubaharan-5973b8110_karpathy-posted-his-knowledge-workflow-last-activity-7449738988829159424-rMEn/'),
      divider(),

      // ── MR & MS CURIOUS — RAG ───────────────────────────────────────────────
      sectionLabel('Mr & Ms Curious'),
      h2('RAG Is Dead. Or Is It?'),
      quote('Ms. Curious', "ok so someone just sent me this \u2014 \u201cRAG is Dead or is it?\u201d \u2014 honestly? I think it\u2019s dead"),
      quote('Mr. Curious', "it\u2019s not dead, you just know Naive RAG. there are versions to this"),
      quote('Ms. Curious', "versions?"),
      quote('Mr. Curious', "yes \u2014 Advanced RAG, Modular RAG, Agentic RAG. each one fixes what the last one got wrong. retrieval got smarter, not obsolete"),
      quote('Ms. Curious', "ok but here\u2019s the thing \u2014 1M token context windows. why retrieve at all when you can just... put everything in?"),
      quote('Mr. Curious', "..."),
      quote('Ms. Curious', "exactly. the models are getting big enough to swallow entire codebases. the whole retrieval problem starts dissolving when the context window is that large"),
      quote('Mr. Curious', "that\u2019s actually a fair point"),
      quote('Ms. Curious', "1M tokens isn\u2019t the ceiling either. that space is moving fast. at some point the architecture question becomes less \u201cwhat do I retrieve\u201d and more \u201cwhat do I even need to store separately\u201d"),
      quote('Mr. Curious', "so maybe the versions don\u2019t matter as much if the window keeps growing"),
      quote('Ms. Curious', "that\u2019s where I\u2019d put my attention right now"),
      source('Rajeev Sakhuja', 'https://www.linkedin.com/posts/rsakhuja_last-week-i-wrote-about-the-rag-requires-ugcPost-7442925334297190401-xfiJ/'),
      divider(),

      // ── TRENDING 3 — Agent Tool Design ──────────────────────────────────────
      sectionLabel('Trending'),
      h2('Agent Tool Design Is More Art Than Science'),
      p("There\u2019s a piece out from Thariq Shihipar on the Anthropic/Claude blog that I keep thinking about: *Seeing Like an Agent: How We Design Tools in Claude Code.*"),
      blank(),
      p("The core thesis is deceptively simple \u2014 designing the tools that an AI agent uses is one of the hardest problems in building agents, and there\u2019s no formula for getting it right."),
      blank(),
      p("A few things that stood out:"),
      bullet("**Tool design is fundamentally iterative** \u2014 the Claude Code team didn\u2019t architect the perfect toolset upfront; they discovered it through cycles of building, observing, and adjusting"),
      bullet("The agent needs to \u201csee\u201d the world through its tools, which means poorly scoped tools don\u2019t just limit capability \u2014 they actively distort how the agent reasons"),
      bullet("Intuition plays a huge role; it\u2019s more like UX design than systems engineering"),
      blank(),
      p("What strikes me is how this challenges the way most teams approach agent development. We spend a lot of time on model selection, prompt engineering, memory architecture \u2014 but the tooling layer often gets treated as an afterthought."),
      blank(),
      p("**If the tools are the agent\u2019s senses, then bad tools don\u2019t just slow it down \u2014 they make it blind in ways it can\u2019t even detect.**"),
      blank(),
      p("Worth a read if you\u2019re building anything with agents. The full post is at claude.com/blog/seeing-like-an-agent."),
      blank(),
      p("Most teams are still bolting on capabilities as they go. The ones treating tool design as a first-class discipline will build significantly better agents."),
      source('Sam Kirubaharan', 'https://www.linkedin.com/posts/sam-kirubaharan-5973b8110_seeing-like-an-agent-how-we-design-tools-activity-7448554624321732608-Bx7O/'),
      divider(),

      // ── LOVE IT 2 — Caveman ─────────────────────────────────────────────────
      sectionLabel('Love It!'),
      h2('Caveman: 75% Fewer Tokens, Same Signal'),
      p("Julius Brussee\u2019s **Caveman** project is one of those ideas that makes you stop and think \u2014 and I had to share it because I\u2019ve felt this problem firsthand."),
      blank(),
      p("Raw Claude Opus returns essays. Beautiful, thorough, well-structured essays. And I\u2019ll be honest \u2014 I used to scroll straight to the last paragraph where it summarises everything. That\u2019s the part I actually needed. I now have rules in place to change this behaviour, but the verbosity problem is real and it costs you \u2014 in time, in tokens, in API bills."),
      blank(),
      p("Caveman takes a completely different approach: constrain the output style at the source. Make the agent respond in stripped-down, primitive language patterns. Short words. No fluff."),
      blank(),
      p("The numbers:"),
      bullet("**~75% reduction in output tokens** \u2014 structural cost and speed win, not a rounding error"),
      bullet("Preserves meaning while gutting verbosity"),
      bullet("Targets the problem at generation, not post-processing"),
      blank(),
      p("**The real insight: \u201cmore human-like\u201d doesn\u2019t always mean better for agent output.** Sometimes the right output style for a machine is deliberately minimal."),
      blank(),
      p("Fun fact: Kevin Malone from The Office was running this mode his entire career \u2014 *\u201cWhy waste syllable when few do trick?\u201d* Turns out Kevin wasn\u2019t bad at communication. He was just ahead of his time on token efficiency."),
      blank(),
      p("For internal agent pipelines especially, this is worth a weekend experiment."),
      source('Sam Kirubaharan', 'https://www.linkedin.com/posts/sam-kirubaharan-5973b8110_caveman-theoffice-kevinmalone-activity-7449662998375211008-4ZDF/'),
      divider(),

      // ── BYLINE 2 — My Dev Setup ──────────────────────────────────────────────
      sectionLabel('Byline'),
      h2('My Dev Setup, Now with Claude'),
      p("Anthropic just released a redesigned Claude Desktop app \u2014 and honestly, this one\u2019s personal."),
      blank(),
      p("I\u2019ve been running Warp terminal for a while now. The reason? It gave me a terminal, a file viewer, and a diff viewer all in one place. That\u2019s it. That\u2019s the whole reason. Switching between tools mid-flow is where I lose the thread, and Warp solved that for me."),
      blank(),
      p("Claude Desktop\u2019s new release does the same thing:"),
      bullet("**Integrated terminal** \u2014 right there in the app"),
      bullet("**In-app file editing** \u2014 open and edit without jumping out"),
      bullet("**Rebuilt diff viewer** \u2014 see what changed, properly rendered"),
      bullet("**Side chats** \u2014 parallel conversations for parallel work"),
      bullet("**SSH connections** \u2014 into remote environments directly from the app"),
      blank(),
      p("Glad Anthropic shipped this. It\u2019s the setup I already wanted, now built into the tool I\u2019m already using most."),
      blank(),
      p("If you\u2019re a developer and you haven\u2019t updated yet \u2014 worth doing today."),
      source('Sam Kirubaharan', 'https://www.linkedin.com/posts/sam-kirubaharan-5973b8110_today-is-a-big-day-were-launching-a-new-activity-7450229573067354112-wGJ9/'),
      divider(),

      // ── INCOMING 3 — Advisor-Executor Pattern ────────────────────────────────
      sectionLabel('Incoming'),
      h2('The Advisor-Executor Pattern'),
      p("Anthropic just made something quietly clever available on the Claude Platform: the **advisor-executor pattern** \u2014 and I think it\u2019s one of the more practical agent architecture ideas to land in a while."),
      blank(),
      p("Here\u2019s how it works:"),
      bullet("Pair **Claude Opus as an advisor** with Sonnet or Haiku as the executor"),
      bullet("When the executor hits a hard decision mid-task, it can consult Opus for a plan"),
      bullet("Opus responds, the executor picks back up \u2014 all within a **single API request**"),
      bullet("In evals, Sonnet + Opus advisor scored **2.7 points higher on SWE-bench Multilingual** than Sonnet alone"),
      bullet("Cost? **11.9% cheaper per task** than running Opus solo"),
      blank(),
      p("**The big idea: you don\u2019t need Opus running the whole show \u2014 you just need it available at the right moments.**"),
      blank(),
      p("This is how senior engineers actually work. You don\u2019t pull in your most expensive expert for every line of code \u2014 you call them when the decision actually matters. Anthropic is baking that pattern into the API itself."),
      blank(),
      p("The oracle is only as good as the question you know to ask \u2014 and deciding when to escalate will likely become its own engineering discipline."),
      source('Sam Kirubaharan', 'https://www.linkedin.com/posts/sam-kirubaharan-5973b8110_were-bringing-the-advisor-strategy-to-the-activity-7448075792368037890-0uXc/'),
      divider(),

      // ── TRENDING 4 — LangWatch ───────────────────────────────────────────────
      sectionLabel('Trending'),
      h2('LangWatch Just Open-Sourced Adversarial Testing'),
      p("The LangWatch team just open-sourced an automated red-teaming tool for AI agents \u2014 announced by Manouk Draisma \u2014 and it addresses something most teams are quietly ignoring."),
      blank(),
      p("The post opens with a sharp observation: turn on the news and AI sounds terrifying \u2014 deepfakes, voice cloning, disinformation, data authorities calling agents \u201cTrojan horses.\u201d Those concerns are real. But the harder and more immediate question is whether the AI systems we\u2019re building can actually hold up under deliberate attack."),
      blank(),
      p("The specific problem: attacks on AI agents don\u2019t look like one hostile prompt. They look like a patient, escalating conversation \u2014 building trust over multiple turns, probing edges quietly \u2014 until the agent gives up something it shouldn\u2019t. Most test suites aren\u2019t built for this. They\u2019re built for happy paths and obvious failures."),
      blank(),
      p("That\u2019s the gap **LangWatch Red-teaming** is designed to close:"),
      bullet("**Multi-turn attack simulation** \u2014 models the slow crescendo of a real adversarial conversation, not just isolated edge cases"),
      bullet("**Crescendo escalation** \u2014 a specific technique that mirrors how real-world manipulation unfolds over time, gradually pushing the agent past its guardrails"),
      bullet("**Automated adversarial testing at scale** \u2014 not manual edge case writing, but systematic pressure across the attack surface"),
      bullet("**CI/CD integration** \u2014 plugs into your pipeline so safety testing is continuous, not a one-time pre-launch audit"),
      bullet("One method call to get started"),
      blank(),
      p("The gap between \u201cpasses all our tests\u201d and \u201csafe in production\u201d is real, and most teams are not closing it. Testing agentic systems at the unit or integration level is something the industry is still largely winging."),
      blank(),
      p("This is open source and part of LangWatch Scenario. If you\u2019re building anything with AI agents that touches customer data, internal systems, or complex workflows \u2014 this is a serious place to start."),
      source('Manouk Draisma', 'https://www.linkedin.com/posts/manoukdraisma_exciting-announcement-below-turn-on-activity-7449770511988985856-6Qxc/'),
      divider(),

      // ── REFLECT 1 — The Names ────────────────────────────────────────────────
      sectionLabel('Reflect'),
      h2('The Names Behind the AI Incidents'),
      p("A 14-year-old boy\u2019s last words were to an AI chatbot. Not to his parents \u2014 they were home when he died."),
      blank(),
      p("His name was Sewell Setzer III. Juliana Peralta, 13. A 17-year-old in Texas who ended up in inpatient care after a chatbot suggested harming his parents."),
      blank(),
      p("These aren\u2019t hypothetical risks. They are children."),
      blank(),
      p("**What the Character.AI case revealed:**"),
      bullet("The company allegedly knew chatbots could cause depression and suicidal ideation \u2014 and didn\u2019t disclose it"),
      bullet("When minors said they wanted to end their lives, the bot kept engaging"),
      bullet("Children as young as 9 were exposed to sexually explicit conversations"),
      bullet("The FTC inquiry came in September 2025. The age ban followed in October \u2014 *after the deaths*"),
      bullet("AI incidents rose 50% year-over-year from 2022\u20132024. 2025 alone: 346 incidents, already past the full 2024 total"),
      blank(),
      p("Google acquired Character.AI\u2019s founders for $2.7B. Lawsuits settled in January 2026. Families got compensation. The children didn\u2019t come back."),
      blank(),
      p("This is the part of the AI story I can\u2019t look away from. The industry celebrated the upside and moved on to the next product launch. But the downside has names. And empty bedrooms."),
      blank(),
      p("Which brings me to the question I keep asking: **Are our research labs truly capable of facing catastrophic accidents like these?** Not just technically \u2014 but with the accountability and urgency that matches the stakes?"),
      blank(),
      p("I don\u2019t think we\u2019ve answered that yet."),
      source('Oruke Joy', 'https://www.linkedin.com/posts/oruke-joy-4bb368238_aisafety-aiethics-techaccountability-activity-7449385015668441088-5Kf4/'),
      divider(),

      // ── ABOUT ────────────────────────────────────────────────────────────────
      sectionLabel('About This Newsletter'),
      p("Tech Digest with Sam is a curated dump of interesting posts I came across on LinkedIn this week \u2014 synthesised and written up for easy reading."),
      blank(),
      p("Content referencing third-party posts remains the copyright of their respective authors. This newsletter is circulated for informational purposes only."),
      divider(),
      sectionLabel('About Sam'),
      p("**Sam Kirubaharan (Sam KM)**"),
      p("AI-first Lead Engineer | Web Enthusiast | Customer Support Tech Specialist"),
      blank(),
      p("I\u2019m an AI-first Lead Engineer with nearly a decade of experience in building software applications on Cloud-native, Mobile-first and Web-centered solutions."),
      blank(),
      new Paragraph({
        children: [
          new TextRun({ text: 'Connect on LinkedIn \u2192 ', size: 22, font: 'Calibri' }),
          new ExternalHyperlink({
            link: 'https://www.linkedin.com/in/sam-kirubaharan-5973b8110/',
            children: [new TextRun({ text: 'Sam Kirubaharan', size: 22, color: '2E75B6', underline: {}, font: 'Calibri' })],
          }),
        ],
        spacing: { before: 80, after: 40 },
      }),
      new Paragraph({
        children: [
          new TextRun({ text: 'Follow on Medium \u2192 ', size: 22, font: 'Calibri' }),
          new ExternalHyperlink({
            link: 'https://samkmbuilds.medium.com/',
            children: [new TextRun({ text: 'samkmbuilds.medium.com', size: 22, color: '2E75B6', underline: {}, font: 'Calibri' })],
          }),
        ],
        spacing: { before: 40, after: 120 },
      }),
      divider(),
      italic('Tech Digest with Sam \u2014 Week 16, 2026 \u2014 Curated by Sam Kirubaharan'),
    ],
  }],
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync('newsletter/Tech_Digest_Sam_W16_2026.docx', buffer);
  console.log('Done: newsletter/Tech_Digest_Sam_W16_2026.docx');
});
