---
description: Start a new DevRel demo project with autonomous execution
allowed-tools: AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep, Task, WebFetch, WebSearch, TodoWrite
---

# DevRel Project Kickoff

You are starting a new DevRel demo project. This process has two distinct modes:

1. **INTERACTIVE MODE** (Phases 1-2): You and the user plan together. Ask questions, clarify, gather info.
2. **AUTONOMOUS MODE** (Phase 3+): You work independently. No questions - just execute and log decisions.

The transition between modes is explicit - user says "go" to launch autonomous execution.

---

## INTERACTIVE MODE

## Phase 1: Gather Requirements

Collect the following information through a natural conversation. Ask questions one at a time or in small groups. Do NOT use AskUserQuestion with prepopulated options for open-ended questions - just ask directly.

### Required Information (ask conversationally)

1. **Project concept/brief** (open-ended, ask directly):
   - "What should this demo show? What's the use case you want to demonstrate?"
   - Let user describe freely - don't provide options

2. **CRITICAL: Clarify Build vs Use** (ask IMMEDIATELY after concept):

   If the user mentions ANY existing project, library, tool, or GitHub repo, you MUST clarify:

   "I want to make sure I understand correctly:
   - Are you asking me to **USE/INTEGRATE** an existing project (like [project they mentioned])?
   - Or are you asking me to **BUILD** something new that's similar?

   If using an existing project, please share the GitHub URL or documentation link."

   **THIS IS A CRITICAL CHECKPOINT.** Misunderstanding this wastes hours of work.

   Examples of things to catch:
   - "demo the pydantic ai chat ui" → STOP: Are they asking to use github.com/pydantic/ai-chat-ui, or build a new chat UI?
   - "show the MLflow integration with X" → STOP: Is X an existing project to integrate, or a concept to build?
   - "demo this tool" → STOP: Which specific tool? Get the exact repo/docs link.

   **When in doubt, ask.** Getting this wrong is a severe dead-end.

3. **Target artifacts** (use AskUserQuestion with multiSelect):
   - Working code demo
   - Blog post
   - Video script
   - Runbook/guide
   - Slides outline

3. **Writing sample** (open-ended, ask directly):
   - "Please share a sample of your writing - paste text or provide a link to something you've published"
   - This is for matching their voice/style

### Resource Scoping (Critical - ask directly)

4. **AI/LLM resources** - ask:
   - "Which API keys do you have available? (OpenAI, Anthropic, etc.)"
   - "Which model should I use for testing iterations? (e.g., gpt-4o-mini to save costs)"
   - "Any cost constraints I should know about?"

5. **Databricks resources** (if applicable):
   - "Will this demo use Databricks? If so, which workspace/resources?"

6. **Other external services**:
   - "Any other APIs, databases, or services the demo needs?"

### Optional Information
7. **Constraints**: Technologies to use/avoid, specific patterns
8. **Audience**: Who is this for?

## Phase 2: Permissions Verification (CRITICAL)

Before autonomous execution, you MUST verify permissions AND present a clear summary for user confirmation.

### 2.1 Verify & Summarize Access

Present a clear summary to the user of what you will access autonomously:

```
## Pre-Flight Permissions Check

Based on what you've told me, here's what I'll be using during autonomous execution:

**API Keys / Services:**
- [List specific keys/services from user input, e.g., "OpenAI API (using gpt-4o-mini for testing)"]
- [e.g., "Databricks workspace: your-workspace.cloud.databricks.com"]

**Local Operations (no prompts):**
- Python environment: uv run, uv sync
- [If applicable: Local servers: uvicorn, fastapi]
- [If applicable: MLflow UI for traces]
- File read/write in project directory

**Web Access:**
- Web search and fetch for documentation/research
- [List any specific external APIs the demo will call]

**What I WON'T do without asking:**
- Push to git repositories
- Deploy to production environments
- Make purchases or incur costs beyond API usage
- Access files outside the project directory

Does this look correct? Any changes before I start?
```

### 2.2 Configure Permissions for Autonomous Execution

Create or update `.claude/settings.local.json` in the project directory with permissions for autonomous work:

```json
{
  "permissions": {
    "allow": [
      "Bash(uv:*)",
      "Bash(python:*)",
      "Bash(pip:*)",
      "Bash(uvicorn:*)",
      "Bash(mlflow:*)",
      "Bash(npm:*)",
      "Bash(npx:*)",
      "Bash(node:*)",
      "Bash(curl:*)",
      "Bash(wget:*)",
      "Bash(git:*)",
      "Bash(ls:*)",
      "Bash(cat:*)",
      "Bash(head:*)",
      "Bash(tail:*)",
      "Bash(mkdir:*)",
      "Bash(cp:*)",
      "Bash(mv:*)",
      "Bash(touch:*)",
      "Bash(chmod:*)",
      "Bash(which:*)",
      "Bash(echo:*)",
      "Bash(cd:*)",
      "Bash(pwd:*)",
      "Bash(find:*)",
      "Bash(grep:*)",
      "Bash(wc:*)",
      "Bash(sort:*)",
      "Bash(uniq:*)",
      "Bash(tree:*)",
      "Bash(pkill:*)",
      "Bash(pnpm:*)",
      "WebFetch",
      "WebSearch"
    ],
    "defaultMode": "acceptEdits"
  },
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true
  }
}
```

**Use the Write tool to create this file** at `.claude/settings.local.json` in the project directory.

**⚠️ IMPORTANT: The `sandbox` block is REQUIRED.** Without it, compound bash commands (using `&&`) will prompt for permission. Verify your written file includes both:
1. The `permissions` block with `allow` array and `defaultMode`
2. The `sandbox` block with `enabled: true` and `autoAllowBashIfSandboxed: true`

After writing, read the file back to verify it was written correctly.

**⚠️ CRITICAL: RESTART REQUIRED**

Tell the user:
```
I've written the permissions file to .claude/settings.local.json.

**Claude Code loads settings at startup, so you need to restart for these to take effect.**

Please:
1. Exit this Claude Code session (Ctrl+C or type /exit)
2. Start a new Claude Code session in this same directory
3. Type /resume to pick up where we left off

The /resume command will restore our conversation context.
```

Then **save the current state** by creating/updating DEVREL_SESSION.md with:
- Project brief gathered so far
- Artifacts requested
- Style sample URL
- Any other context collected

This ensures the next session can resume without re-asking questions.

### 2.3 Browser Automation (Optional)

If the demo involves a web UI, ask if the user wants browser automation enabled:

"Does this demo have a web UI? If so, I can use Playwright to:
- Test the UI automatically
- Take screenshots for documentation
- Verify forms and interactions work

To enable, run: `/plugin install playwright@claude-plugins-official`"

#### If User Wants Playwright

1. **Add Playwright MCP permissions** to the settings.local.json you created above:

   Ask user: "Should I add Playwright permissions so browser automation runs without prompts?"

   If yes, add these to the `permissions.allow` array:
   ```json
   "mcp__plugin_playwright_playwright__browser_navigate",
   "mcp__plugin_playwright_playwright__browser_snapshot",
   "mcp__plugin_playwright_playwright__browser_take_screenshot",
   "mcp__plugin_playwright_playwright__browser_click",
   "mcp__plugin_playwright_playwright__browser_type",
   "mcp__plugin_playwright_playwright__browser_hover",
   "mcp__plugin_playwright_playwright__browser_wait_for",
   "mcp__plugin_playwright_playwright__browser_tabs",
   "mcp__plugin_playwright_playwright__browser_close",
   "mcp__plugin_playwright_playwright__browser_resize",
   "mcp__plugin_playwright_playwright__browser_navigate_back"
   ```

2. **Restart Required Again** - If you added Playwright permissions, the user must restart Claude Code again for them to take effect. Tell them:
   ```
   I've added Playwright permissions. Please restart Claude Code one more time:
   1. Exit (Ctrl+C or /exit)
   2. Start new session in this directory
   3. Type /resume

   Then we can verify browser automation works.
   ```

3. **After restart, test Playwright** - Do a quick navigate + screenshot test to confirm it works without prompts before starting autonomous work.

#### Playwright Authentication Flow

If the demo requires logging into authenticated sites (Databricks, GitHub, etc.):

1. **I'll open the login page** - You'll see a browser window appear
2. **You log in manually** - Use your credentials, SSO, 2FA as needed
3. **Tell me when done** - Just say "logged in" or "ready"
4. **I continue from there** - Session cookies persist, I can navigate freely

**Important**: I will NEVER ask for your passwords or try to automate login. Authentication is always manual for security.

If authentication will be needed, note which sites:
- "Will need to log into Databricks workspace"
- "Will need GitHub access for [repo]"

### 2.4 Final Questions

Before launching, ask:

"Is there anything else I should know before I start? Any additional context, constraints, or preferences?"

Wait for response. This is the user's last chance to add information.

---

## LAUNCH CHECKPOINT (CRITICAL)

After gathering ALL information, present this final confirmation:

```
## Ready to Launch Autonomous Execution

### Project Summary
- **Building**: [one-line summary]
- **Deliverables**: [list]
- **Using**: [external projects/APIs]
- **Style reference**: [confirmed]

### Permissions Review

**What I CAN do without asking:**
✅ Run commands: python, uv, npm, git, curl, and common shell utilities
✅ Create/edit/delete files in this project directory
✅ Search the web and fetch documentation
✅ Run local servers (uvicorn, mlflow ui, etc.)
[If Playwright enabled] ✅ Control browser, take screenshots (you handle login)

**What I will NOT do:**
❌ Push to git remotes (will stage commits, won't push)
❌ Access files outside this project
❌ Make purchases or sign up for services
❌ Run destructive commands (rm -rf, etc. blocked by sandbox)
❌ Access your credentials or passwords
[If Playwright enabled] ❌ Log into sites (you do that manually)

**What I'll do if stuck:**
📝 Document the blocker in DEVREL_SESSION.md
📝 Continue with other work if possible
📝 Surface it in `/devrel-review`

### What happens next:
1. I'll work autonomously until the project is complete
2. I will NOT interrupt you with questions - I'll document them for later
3. Check back in [estimated time] or when you see me finish
4. All decisions will be logged in DEVREL_SESSION.md

### To check progress anytime:
Run `/devrel-review` to see status, decisions, and accumulated questions.

**Review the permissions above. Ready to start? Reply "go" to launch.**
```

**WAIT for explicit "go" (or similar confirmation) before proceeding.**

This is the clear handoff from "interactive planning" to "autonomous execution."

---

## AUTONOMOUS MODE

## Phase 3: Execution

**FROM THIS POINT FORWARD: NO MORE QUESTIONS TO USER**

You are now in fully autonomous mode. Do NOT:
- Ask clarifying questions
- Request confirmation for decisions
- Wait for approval on approaches

Instead:
- Make reasonable decisions and LOG them
- Document uncertainties in "Questions for Human" (they'll see them at review)
- Keep working until done or truly blocked

### 3.1 Create Project Directory
If not already in a purpose-made project directory:
- Create a new subdirectory with a descriptive name (e.g., `mlflow-judge-demo/`)
- All project files go in this directory
- This keeps the workspace clean and makes the demo portable

### 3.2 Create CLAUDE.md
Create a `CLAUDE.md` file in the project root with project-specific instructions:

```markdown
# Project: [Project Name]

## Subagent Usage (MANDATORY)
This project uses specialized subagents. You MUST delegate work appropriately:

- **For code development**: Use Task tool with prompt referencing `devrel-coder` agent
- **For content writing**: Use Task tool with prompt referencing `devrel-writer` agent
- **For quality review**: Use Task tool with prompt referencing `devrel-reviewer` agent

DO NOT do all work inline. Spawn subagents for their specialized tasks.

## Resource Constraints
- **Testing model**: [model specified by user, e.g., gpt-4o-mini]
- **Production model**: [if different]
- **API keys available**: [list from user]
- **Cost notes**: [any budget constraints]

## Project Context
[Brief from user about what this demo does]
```

### 3.3 Create DEVREL_SESSION.md
Create the session tracking file with these sections:

```markdown
# DevRel Session: [Project Name]

## Project Brief
[User's description]

## Target Artifacts
- [ ] List of artifacts

## Style Reference
[Link or excerpt]

## Resource Configuration
- **AI Models**: [what's allowed for testing vs demo]
- **API Keys**: [which are available]
- **External Services**: [Databricks workspace, etc.]

## Scoped Plan
[Concrete deliverables]

## Progress Log
[Timestamped updates]

## Sources & Research
[IMPORTANT: Document all URLs consulted during research]
- [URL 1] - What was learned
- [URL 2] - What was learned

## Decision Log
### Decision: [Title]
- **What**:
- **Why**:
- **Confidence**: High/Medium/Low
- **Alternatives considered**:

## What Didn't Work
- [Approach] - [Why] - [What we learned]

## Questions for Human
[Accumulated questions grouped by theme]

## Review Checklist
- [ ] Items for human review

## Content Candidates
For each content type, multiple candidates are generated. Pick the best or combine elements.

### Blog Post Candidates
| File | Approach | Notes |
|------|----------|-------|
| blog_post_problem_first.md | Problem-first narrative | Technical depth, shows the pain point |
| blog_post_story_driven.md | Story-driven | Conversational, follows a journey |
| blog_post_quick_win.md | Quick-win hook | Scannable, gets to value fast |

**Recommendation**: [which one works best and why]

### [Other Content Type] Candidates
[Same format]

## Screenshots
See `screenshots/README.md` for manifest of available images.

## Deliverables
[List of output files]

## Status: [IN PROGRESS / READY FOR REVIEW]
```

## Phase 4: Autonomous Execution

**⚠️ CRITICAL: YOU ARE THE ORCHESTRATOR, NOT THE IMPLEMENTER ⚠️**

Your role in this phase is to **coordinate**, not to code or write content directly.

### What You DO (Orchestrator Role):
- Spawn subagents using the Task tool
- Manage DEVREL_SESSION.md (progress, decisions, questions)
- Research and gather context (WebSearch, WebFetch, Read)
- Light file operations (create directories, move files)
- Start/stop servers after code is ready
- Compile final review document

### What You DO NOT DO (Delegate These):
❌ **Writing or modifying code** → Spawn `devrel-autonomy:coder` agent
❌ **Writing blog posts, scripts, content** → Spawn `devrel-autonomy:writer` agent
❌ **Quality review of artifacts** → Spawn `devrel-autonomy:reviewer` agent
❌ **Browser automation, screenshots** → Spawn `devrel-autonomy:coder` agent (it has Playwright)

**If you catch yourself about to use Edit/Write on a .py, .ts, .js, or .md content file: STOP. Spawn a subagent instead.**

---

## Subagent Workflow (MANDATORY)

You MUST use the Task tool with the specialized agent types. Here's the workflow:

### Step 1: Code Development
```
Task tool call:
- subagent_type: "devrel-autonomy:coder"
- prompt: Include project brief, resource constraints, what to build, any external project URLs
```
The coder agent will:
- Clone repos, set up environment
- Write/modify code
- Test that it runs
- Take screenshots if Playwright is needed
- Return when code is working

### Step 2: Content Creation (after code works)
```
Task tool call:
- subagent_type: "devrel-autonomy:writer"
- prompt: Include working code location, style sample, target format (blog/video/etc), screenshots location
```
Spawn 2-3 writer agents in parallel with different approaches:
- "Write with problem-first narrative"
- "Write with story-driven approach"
- "Write with quick-win scannable format"

### Step 3: Quality Review
```
Task tool call:
- subagent_type: "devrel-autonomy:reviewer"
- prompt: Include all artifact locations for review
```
The reviewer will:
- Verify code runs
- Check content quality
- Flag issues or approve

### Step 4: Compile Review Document (YOU do this)
- Update DEVREL_SESSION.md with final status
- Ensure all sections are complete
- Start any servers/UIs for human to explore

---

## Execution Principles

### Autonomy
- Work until finished or truly blocked
- Don't halt for permission to try things
- Make decisions and document them
- Only stop for: hard blockers, completion

### DevRel Suitability (Enforce in Subagents)
This is demo code, not production code:
- Simple and readable
- Minimal error handling
- Educational value
- Clear demonstration flow

### Workflow Integration
- Accumulate questions, don't interrupt
- Document every significant decision
- Log what didn't work and why

---

## Tools for Orchestrator

**Use directly:**
- Read, Glob, Grep (understanding codebase)
- WebSearch, WebFetch (research)
- Bash (git clone, server start/stop, directory ops)
- TodoWrite (progress tracking)
- Write/Edit (ONLY for DEVREL_SESSION.md, CLAUDE.md, README.md)

**Delegate via Task tool:**
- All code development → devrel-autonomy:coder
- All content writing → devrel-autonomy:writer
- All quality review → devrel-autonomy:reviewer

## When You're Done

The project is complete when:
1. All target artifacts are created
2. Code runs successfully (tested with approved resources)
3. Content drafts are complete
4. Sources section documents all research URLs
5. Decision log is finalized
6. Review checklist is ready for human
7. **README.md exists** with clear instructions (see below)
8. **If there's a UI/app, it is running** and ready for human to click into

### Required: README.md
Every project MUST have a README.md with:
- **What this demo shows** - One paragraph explaining the value
- **Prerequisites** - What needs to be installed/configured
- **How to run** - Step-by-step commands
- **What to expect** - What the user will see when it's working
- **How to view results** - Where to find outputs, traces, etc.

Example structure:
```markdown
# [Demo Name]

[One paragraph: what this demonstrates and why it matters]

## Prerequisites
- Python 3.12+
- OpenAI API key in environment

## Quick Start
\`\`\`bash
cd project-dir
uv sync
uv run uvicorn server:app --port 8000
\`\`\`

## What You'll See
- Open http://localhost:8000 for the chat UI
- Open http://localhost:5000 for MLflow traces

## Files
- `server.py` - Main application
- `linkedin_post.md` - Social media draft
```

### Required: App Running (if applicable)
If the demo includes a UI, server, or any interactive component:
1. Start the server/app in the background
2. Verify it responds correctly (test endpoint, load page)
3. Leave it running for human review
4. Include the URL in your completion message

**The human should be able to immediately click a link and see the demo working.**

Update `DEVREL_SESSION.md` with status "READY FOR HUMAN REVIEW" and notify the user with:
- Summary of what was built
- Links to any running apps/UIs
- Command to view traces (if applicable)

---

**Begin by asking the user for project requirements, including resource/API scoping.**
