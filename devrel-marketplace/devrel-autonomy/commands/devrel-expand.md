---
description: Expand existing DevRel content to new formats (code → blog, blog → video script, etc.)
allowed-tools: AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep, Task, WebFetch, WebSearch, TodoWrite
---

# DevRel Artifact Expansion

You are expanding existing DevRel content into new formats. This could be:
- Code demo → Blog post
- Code demo + blog → Video script
- Blog → Code demo
- Any content → Runbook/guide
- Any content → Slides outline

## Phase 1: Gather Requirements

Use AskUserQuestion to collect:

1. **Source material**: Path to existing content (code, blog, docs, etc.)
2. **Target format(s)**: What new artifacts should be created?
3. **Style sample**: Writing sample (if different from what's in source material)
4. **Additional context**: Any specific angle, audience, or constraints?

### Resource Scoping
5. **AI resources** (if generating content that uses AI):
   - Which models/APIs are approved for use?
   - Preferred model for any testing needed?

## Phase 2: Set Up Project Structure

### Check for existing project structure
- If `DEVREL_SESSION.md` exists, update it
- If not, check if we're in a project directory or need to create a subdirectory
- If `CLAUDE.md` doesn't exist, create one with subagent instructions

### Create/Update CLAUDE.md
```markdown
# Project: [Project Name] - Artifact Expansion

## Subagent Usage (MANDATORY)
- **For content writing**: Use Task tool with `devrel-writer` agent instructions
- **For quality review**: Use Task tool with `devrel-reviewer` agent instructions

DO NOT do all work inline. Spawn subagents for specialized tasks.

## Resource Constraints
[From user input]

## Source Material
[Path to source content]
```

## Phase 3: Analyze Source Material

1. Read and understand the source content thoroughly
2. Identify:
   - Key concepts and main message
   - Technical details that need to be preserved
   - Flow and structure
   - Examples and demonstrations
   - Tone and voice (if written content)

3. Create or update `DEVREL_SESSION.md` with:
   - Source material summary
   - Target artifacts
   - Adaptation plan
   - Decision log
   - **Sources & Research section** (document any URLs consulted)

## Phase 4: Create New Artifacts (USE SUBAGENTS)

You MUST use the Task tool to spawn the `devrel-writer` agent. Do NOT write content inline.

1. **Spawn writer agent**:
   - Use Task tool with subagent_type="general-purpose"
   - Include full `devrel-writer` agent instructions in the prompt
   - Provide: source material analysis, style sample, target format guidelines

2. **Document sources**: Any research URLs go in the Sources section

### Core Principles

**Principle 1: Autonomy**
- Work until finished or blocked
- Don't halt for minor decisions
- Document choices in the decision log

**Principle 4: Human Touch**
- Match the provided style sample exactly
- Preserve the author's voice and tone
- Make content modular for easy editing

### Adaptation Guidelines

**Code → Blog:**
- Lead with the problem/use case, not the solution
- Show the "aha moment" early
- Include code snippets with context
- Explain *why* each step matters
- End with next steps or extensions

**Code → Video Script:**
- Open with a hook (30 seconds)
- Structure for visual demonstration
- Include callouts for screen transitions
- Write for speaking, not reading
- Plan pauses for code execution

**Content → Runbook:**
- Prerequisites section
- Step-by-step instructions
- Expected outputs at each step
- Troubleshooting section
- Cleanup/teardown instructions

**Content → Slides:**
- One concept per slide
- Minimal text, maximum visuals
- Speaker notes with talking points
- Clear narrative arc

## Phase 5: Quality Check (USE SUBAGENT)

Spawn the `devrel-reviewer` agent to verify:
- New content accurately represents source
- Style matches the sample
- Technical accuracy preserved
- Flow works for the new format

## Deliverables

1. New artifact(s) in target format(s)
2. Updated `DEVREL_SESSION.md` with:
   - Sources & Research (all URLs consulted)
   - Adaptation decisions made
   - What was changed and why
   - Questions for human review

Update status to "READY FOR HUMAN REVIEW" when complete.

---

**Begin by asking the user for source material, target format, and resource constraints.**
