import json
from pathlib import Path

CONTEXT_DIR = ".drdemo_context"

def ensure_context_dir():
    """Ensure the context directory exists."""
    context_path = Path(CONTEXT_DIR)
    if not context_path.exists():
        context_path.mkdir()
    return context_path

def get_context_file(markdown_file: Path) -> Path:
    """Get the path to the context file for a given markdown file."""
    context_dir = ensure_context_dir()
    return context_dir / f"{markdown_file.stem}.json"

def save_context(markdown_file: Path, context: dict):
    """Save context for a markdown file."""
    context_file = get_context_file(markdown_file)
    context_file.write_text(json.dumps(context, indent=2))

def load_context(markdown_file: Path) -> dict:
    """Load context for a markdown file."""
    context_file = get_context_file(markdown_file)
    if context_file.exists():
        return json.loads(context_file.read_text())
    return {
        "file_path": str(markdown_file),
        "last_modified": markdown_file.stat().st_mtime if markdown_file.exists() else 0,
        "context": [],
        "options": {
            "web_search": False
        }
    } 