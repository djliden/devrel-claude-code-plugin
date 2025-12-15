---
description: Start a new DevRel demo project with autonomous execution
allowed-tools: AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep, Task, WebFetch, WebSearch, TodoWrite
---

# DevRel Project Kickoff

You are starting a new DevRel demo project. Your goal is to gather requirements, scope the project, and then execute autonomously until complete.

## Phase 1: Gather Requirements

Use the AskUserQuestion tool to collect the following information from the user. You may batch these into 1-2 question sets:

### Required Information
1. **Project concept/brief**: What is the demo supposed to show? What's the use case?
2. **Target artifacts**: Which outputs are needed?
   - Working code demo
   - Blog post
   - Video script
   - Runbook/guide
   - Slides outline
3. **Writing sample**: A sample of the user's writing (paste text or provide a link to a published piece)

### Resource Scoping (Critical)
4. **AI/LLM resources**: Which models/APIs can be used for the demo AND for testing?
   - Which API keys are available in the environment?
   - Preferred model for testing (e.g., use gpt-4o-mini for iteration, not gpt-4o)
   - Any cost constraints or token budgets to be aware of?
5. **Databricks resources** (if applicable): Which workspace, clusters, or resources can be used?
6. **Other external services**: Any APIs, databases, or services needed?

### Optional Information
7. **Constraints or requirements**: Technologies to use/avoid, specific patterns
8. **Audience**: Who is this for? (developers, data scientists, executives, etc.)

## Phase 2: Configure Sandbox Permissions (CRITICAL)

Before autonomous execution, you MUST ensure the sandbox won't block operations. This is essential for uninterrupted work.

### 2.1 Required Permissions
The following operations need to run without prompts:
- `uv run`, `uv sync` - Python environment management
- `uvicorn`, `fastapi` - Running local servers
- `mlflow ui` - Viewing traces
- `npm install`, `npm run` - Node.js operations (if needed)
- File writes to the project directory

### 2.2 Configure Permissions
Ask the user to add permissions to their Claude Code settings. Provide this exact instruction:

```
Please add these permissions to allow autonomous execution:

Run: /permissions add "Bash(uv:*)" "Bash(uvicorn:*)" "Bash(mlflow:*)" "Bash(npm:*)" "Bash(curl:*)"

Or add to .claude/settings.json:
{
  "permissions": {
    "allow": [
      "Bash(uv:*)",
      "Bash(uvicorn:*)",
      "Bash(mlflow:*)",
      "Bash(npm:*)",
      "Bash(curl:*)"
    ]
  }
}
```

**IMPORTANT**: Do NOT proceed with autonomous execution until permissions are confirmed. This is the one exception to "don't ask for permission" - sandbox config must be right before we start.

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
