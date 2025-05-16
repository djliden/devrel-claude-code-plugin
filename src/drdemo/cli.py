import os
import click
from pathlib import Path
from .tui import TutorialGenerator
from .context import load_context, save_context

@click.group()
def main():
    """AI-powered tutorial and guide generation tool."""
    pass

@main.command()
def init():
    """Initialize a new tutorial project in the current directory."""
    # Create untitled.md if it doesn't exist
    untitled_path = Path("untitled.md")
    if not untitled_path.exists():
        untitled_path.write_text("# Untitled Tutorial\n\n## Outline\n\n")
        click.echo(f"Created {untitled_path}")
    
    # Initialize context
    context = load_context(untitled_path)
    save_context(untitled_path, context)
    
    # Launch the TUI
    app = TutorialGenerator(untitled_path)
    app.run()

@main.command()
@click.argument('filename')
def edit(filename):
    """Edit an existing tutorial file."""
    file_path = Path(filename)
    if not file_path.exists():
        click.echo(f"Error: File {filename} does not exist")
        return
    
    # Load or initialize context
    context = load_context(file_path)
    save_context(file_path, context)
    
    # Launch the TUI
    app = TutorialGenerator(file_path)
    app.run()

if __name__ == "__main__":
    main() 