---
description: Review session status after autonomous execution - see progress, decisions, and questions
allowed-tools: Read, Glob, Grep, AskUserQuestion, Write, Edit, Task, Bash, TodoWrite
---

# DevRel Session Review

The human is returning to review autonomous work. Present a clear, actionable summary.

## Locate Session Files

1. Find `DEVREL_SESSION.md` in the project directory
2. Also check for `CLAUDE.md` (project-specific instructions)
3. If not found, search for recent work files and summarize what's available

## Present Review Summary

Read and present the following from `DEVREL_SESSION.md`:

### 1. Progress Summary
- What was accomplished
- What artifacts were created
- Current status (complete, in progress, blocked)

### 2. Sources & Research
**IMPORTANT**: Present all URLs that were consulted during research:
- List each source with what was learned from it
- This allows the human to quickly verify information
- Flag if Sources section is missing or incomplete

### 3. Decision Log
Present decisions made during autonomous work:
- What was decided
- Why (rationale)
- Confidence level
- Any alternatives considered

### 4. What Didn't Work
- Approaches that were tried and failed
- Why they didn't work
- What was learned

### 5. Resource Usage
- What AI models/APIs were used
- Any cost implications to note
- Were resource constraints followed?

### 6. Questions for Human
Present accumulated questions grouped by theme:
- Technical decisions
- Style/content choices
- Scope clarifications
- Blockers needing resolution

### 7. Review Checklist
Create an actionable checklist for the human:
```
[ ] Review code demo - runs correctly?
[ ] Review blog/content draft - tone matches your voice?
[ ] Verify sources - check key URLs for accuracy?
[ ] Approve/modify technical decisions
[ ] Answer accumulated questions
[ ] Identify any gaps or missing pieces
```

## Quality Checks

Before presenting to human, verify:
- [ ] Sources section exists and has URLs (flag if missing)
- [ ] Decision log has entries (flag if empty)
- [ ] All target artifacts exist
- [ ] Code files are runnable (optionally test)

## Interactive Review

After presenting the summary, ask the human:

1. "Which items need your attention first?"
2. "Are there any decisions you want to revisit?"
3. "Would you like me to verify any of the sources?"
4. "Should I continue working on anything, or is this ready for final polish?"

## If Work Needs Continuation

If the human identifies issues or wants changes:
1. Update the todo list with new tasks
2. Update `DEVREL_SESSION.md` with human feedback
3. Read `CLAUDE.md` for project-specific instructions (especially subagent usage)
4. Resume autonomous execution following the principles

## If Ready for Finalization

If the human approves the work:
1. Note any final polish items they'll handle
2. Mark the session as complete in `DEVREL_SESSION.md`
3. Summarize what's ready for publication/sharing
4. List the deliverable files and their locations

---

**Begin by finding and reading the session file and CLAUDE.md.**
