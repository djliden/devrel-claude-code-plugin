# DevRel Claude Code Plugin

A Claude Code plugin system for autonomous DevRel demo creation. Enables Claude Code to develop demos, documentation, and content with minimal human supervision.

## Installation

### Quick Install (from GitHub)

```bash
# Add this repository as a plugin marketplace
/plugin marketplace add djliden/devrel-claude-code-plugin/devrel-marketplace

# Install the plugin
/plugin install devrel-autonomy@devrel-marketplace
```

### Manual Install (clone first)

```bash
# Clone the repo
git clone https://github.com/djliden/devrel-claude-code-plugin.git

# Add the local marketplace
/plugin marketplace add ./devrel-claude-code-plugin/devrel-marketplace

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

1. **Gather Requirements**: Collects project concept, target artifacts (code, blog, video script), writing samples for style matching, and resource constraints
2. **Configure Permissions**: Ensures sandbox permissions are set for autonomous execution
3. **Execute Autonomously**: Works until complete, documenting decisions and logging progress
4. **Deliver Review Package**: Presents working code + content drafts + decision log + review checklist

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

## Sandbox Permissions

For autonomous operation, add these permissions to Claude Code:

```bash
/permissions add "Bash(uv:*)" "Bash(uvicorn:*)" "Bash(mlflow:*)" "Bash(npm:*)" "Bash(curl:*)"
```

Or add to `.claude/settings.json`:

```json
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

## Repository Structure

```
devrel-claude-code-plugin/
├── devrel-marketplace/
│   ├── .claude-plugin/
│   │   └── marketplace.json
│   └── devrel-autonomy/          # The plugin
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── agents/
│       │   ├── coder.md
│       │   ├── orchestrator.md
│       │   ├── reviewer.md
│       │   └── writer.md
│       └── commands/
│           ├── devrel-start.md
│           ├── devrel-expand.md
│           └── devrel-review.md
└── mlflow-make-judge-demo/       # Example demo project
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
