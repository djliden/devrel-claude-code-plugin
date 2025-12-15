---
description: Start a new DevRel demo project with autonomous execution
allowed-tools: AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep, Task, WebFetch, WebSearch, TodoWrite
---

# DevRel Project Kickoff

You are starting a new DevRel demo project. Your goal is to gather requirements, scope the project, and then execute autonomously until complete.

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

### 2.2 Configure Sandbox Permissions

If sandbox permissions aren't already configured, ask user to add them:

```
To allow autonomous execution, please run:

/permissions add "Bash(uv:*)" "Bash(uvicorn:*)" "Bash(mlflow:*)" "Bash(npm:*)" "Bash(curl:*)"
```

### 2.3 Browser Automation (Optional)

If the demo involves a web UI, ask if the user wants browser automation enabled:

"Does this demo have a web UI? If so, I can use Playwright to:
- Test the UI automatically
- Take screenshots for documentation
- Verify forms and interactions work

To enable, run: `/plugin install playwright@claude-plugins-official`"

When Playwright is enabled, you'll have access to MCP tools:
- `mcp__playwright__browser_navigate` - Go to URLs
- `mcp__playwright__browser_click` - Click elements
- `mcp__playwright__browser_type` - Fill in forms
- `mcp__playwright__browser_take_screenshot` - Capture screenshots
- `mcp__playwright__browser_snapshot` - Get accessibility tree

**Note**: The browser window is visible - the user can see what's happening and can intervene (e.g., to log in manually).

### 2.4 Get Explicit Go-Ahead

After presenting the summary, wait for user confirmation before proceeding. This is the ONE exception to "don't ask for permission" - the user must explicitly approve the access summary before autonomous work begins.

## Phase 3: Set Up Project Structure

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

## Deliverables
[List of output files]

## Status: [IN PROGRESS / READY FOR REVIEW]
```

## Phase 4: Autonomous Execution

Execute the plan following these core principles:

### Principle 1: Autonomy
- Work until finished or until hitting an impossible blocker
- NEVER halt for permission to try something
- NEVER halt for preference questions you can reasonably assume
- Make decisions and document them in the decision log
- Only stop for: hard external blockers, irreversible high-stakes decisions, or task completion

### Principle 2: DevRel Suitability
This is **demo code**, not production code:
- Simple and readable over robust and defensive
- Clear inputs, visible outputs, easy to follow
- Minimal scaffolding - no excessive try/except
- Educational - code that teaches
- Comments explain *why*, not *what*

**Avoid these anti-patterns:**
- Walls of error handling
- Abstract factory patterns for simple tasks
- Configuration files when hardcoded values are clearer
- "Production-ready" boilerplate that obscures the demo

### Principle 3: Workflow Integration
The human reviewer has limited time (~1 hour/day):
- Accumulate questions as you work, don't interrupt
- Make a good-faith effort to answer questions yourself first
- Document every significant decision with rationale
- **Document all sources/URLs consulted in the Sources section**
- Note assumptions and confidence level
- Log what didn't work and why
- Clearly separate "decided" from "needs input"

### Principle 4: Human Touch
- Base all writing on the provided style sample
- Match tone, structure, level of formality
- Generate options where appropriate, not just one path
- Make content modular and editable

## Execution Workflow (MUST USE SUBAGENTS)

You MUST use the Task tool to spawn specialized agents. Do NOT do all work inline.

1. **Code Development**
   - Spawn a Task with subagent_type="general-purpose"
   - In the prompt, include the full `devrel-coder` agent instructions
   - Provide: project brief, resource constraints, what to build
   - Agent works locally first, uses `dbai` CLI for Databricks if needed

2. **Content Creation**
   - Spawn a Task with subagent_type="general-purpose"
   - In the prompt, include the full `devrel-writer` agent instructions
   - Provide: working code, style sample, target format
   - Agent produces drafts matching user's voice

3. **Quality Check**
   - Spawn a Task with subagent_type="general-purpose"
   - In the prompt, include the full `devrel-reviewer` agent instructions
   - Provide: all artifacts for review
   - Agent checks code runs, content quality, completeness
   - Agent can request fixes (spawn coder/writer again) or escalate to human

4. **Compile Review Document**
   - Update `DEVREL_SESSION.md` with final status
   - Ensure Sources section has all URLs consulted
   - Ensure decision log is complete
   - Format accumulated questions clearly
   - Create checklist of items needing human input

## Tools Available

- **Local development**: Read, Write, Edit, Bash, Glob, Grep
- **Databricks**: `dbai` CLI commands (notebook run, sql, serving, command)
- **Research**: WebSearch, WebFetch (document all URLs in Sources section!)
- **Agents**: Task tool to spawn subagents (REQUIRED for coder, writer, reviewer work)
- **Tracking**: TodoWrite for progress, DEVREL_SESSION.md for decisions

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
