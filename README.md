# DevRel Claude Code Plugin

A Claude Code plugin system for autonomous DevRel demo creation. Enables Claude Code to develop demos, documentation, and content with minimal human supervision.

## Installation

### Quick Install (from GitHub)

```bash
# Add this repository as a plugin marketplace
/plugin marketplace add djliden/devrel-claude-code-plugin

# Install the plugin
/plugin install devrel-autonomy@devrel-marketplace
```

### Manual Install (clone first)

```bash
# Clone the repo
git clone https://github.com/djliden/devrel-claude-code-plugin.git

# Add the local marketplace
/plugin marketplace add ./devrel-claude-code-plugin

# Install the plugin
/plugin install devrel-autonomy@devrel-marketplace
```

## Available Commands

Once installed, you'll have access to these slash commands:

| Command | Description |
|---------|-------------|
| `/devrel-start` | Start a new DevRel demo project with autonomous execution |
| `/devrel-expand` | Expand existing content to new formats (code → blog, etc.) |
| `/devrel-review` | Review session status, decisions, and questions |

## How It Works

### `/devrel-start` - New Project Kickoff

1. **Gather Requirements**: Collects project concept, target artifacts, writing samples for style matching, and resource constraints
2. **Clarify Build vs Use**: If you mention an existing project/tool, confirms whether to USE it or BUILD something new (prevents wasted effort)
3. **Permissions Verification**: Shows exactly what will be accessed (API keys, services, local ops) and gets explicit approval
4. **Browser Setup** (optional): If demo has a web UI, offers Playwright integration for testing and screenshots
5. **Execute Autonomously**: Works until complete, documenting decisions and logging progress
6. **Deliver Review Package**: Presents working code + content drafts + decision log + review checklist

### `/devrel-expand` - Artifact Expansion

Transform existing content into new formats:
- Code demo → Blog post
- Blog post → Video script
- Any combination → Runbook/guide

### `/devrel-review` - Session Review

Check progress on autonomous sessions:
- Summary of accomplishments
- Decision log with rationale
- Accumulated questions
- Items needing human input

## Design Principles

### Autonomy
- Works until finished or hitting an impossible blocker
- Makes decisions and documents them (doesn't halt for permission)
- Only stops for: hard external blockers, irreversible high-stakes decisions, or completion

### DevRel Suitability
Demo code, not production code:
- Simple and readable over robust and defensive
- Clear inputs, visible outputs, easy to follow
- Educational - code that teaches

### Human Touch
- Matches provided writing style samples
- Generates options, not just one path
- Human is editor-in-chief, not proofreader

## Permissions Setup

The plugin automatically creates `.claude/settings.local.json` during setup with permissions for autonomous work. This includes:

- **Sandbox mode**: Safe execution boundaries
- **Auto-approve bash**: Common commands (uv, python, git, npm, etc.) run without prompts
- **Auto-approve edits**: File changes don't require confirmation

If you want to set this up manually, create `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(uv:*)", "Bash(python:*)", "Bash(pip:*)",
      "Bash(uvicorn:*)", "Bash(mlflow:*)",
      "Bash(npm:*)", "Bash(npx:*)", "Bash(node:*)",
      "Bash(curl:*)", "Bash(git:*)",
      "WebFetch", "WebSearch"
    ],
    "defaultMode": "acceptEdits"
  },
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true
  }
}
```

**Key settings:**
- `defaultMode: "acceptEdits"` - Auto-approves file edits
- `sandbox.autoAllowBashIfSandboxed: true` - Auto-approves bash commands within sandbox safety boundaries

## Specialized Agents

The plugin uses specialized subagents for different tasks:

| Agent | Purpose |
|-------|---------|
| **orchestrator** | Coordinates workflow, manages session file, delegates to other agents |
| **coder** | Writes demo code - simple, readable, educational (not production code) |
| **writer** | Creates content (blogs, scripts) matching your writing style |
| **reviewer** | QA check before human review - verifies code runs, content matches style |
| **browser** | Playwright-based UI testing, screenshots, web interaction |

## Browser Automation (Optional)

For demos with web UIs, install the Playwright plugin:

```bash
/plugin install playwright@claude-plugins-official
```

This enables:
- Automated UI testing
- Screenshot capture for documentation
- Form filling and interaction verification
- Works with authenticated sites (you log in manually, Claude continues)

## Repository Structure

```
devrel-claude-code-plugin/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace manifest (must be at repo root)
└── devrel-autonomy/              # The plugin
    ├── .claude-plugin/
    │   └── plugin.json
    ├── agents/
    │   ├── browser.md            # UI testing and screenshots
    │   ├── coder.md              # Demo code development
    │   ├── orchestrator.md       # Workflow coordination
    │   ├── reviewer.md           # Quality assurance
    │   └── writer.md             # Content creation
    └── commands/
        ├── devrel-start.md
        ├── devrel-expand.md
        └── devrel-review.md
```

## Example Usage

```
> /devrel-start

# System asks for:
# - Project concept (what does the demo show?)
# - Target artifacts (code, blog, video script?)
# - Writing sample (for style matching)
# - Resource constraints (which APIs/models to use?)

# Then works autonomously, delivering:
# - Working code + README
# - Content drafts
# - Decision log
# - Review checklist
```

## License

MIT
