import asyncio
import click
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.panel import Panel
from drdemo.agents import ChatManager

console = Console()

def print_response(response):
    """Print the response in a nicely formatted panel."""
    console.print(Panel(
        Markdown(str(response)),
        title="[bold blue]Editor[/bold blue]",
        border_style="blue"
    ))

async def chat_loop():
    """Run the interactive chat loop."""
    console.print("[bold green]Welcome to the Chat Interface![/bold green]")
    console.print("Type 'exit' or 'quit' to end the session.")
    
    # Initialize the chat manager
    chat_manager = ChatManager()
    
    while True:
        try:
            # Get user input
            user_input = Prompt.ask("\n[bold yellow]You[/bold yellow]")
            
            # Check for exit commands
            if user_input.lower() in ['exit', 'quit']:
                console.print("[bold red]Goodbye![/bold red]")
                break
            
            # Get response from editor
            response = await chat_manager.run_editor(user_input)
            print_response(response)
            
        except KeyboardInterrupt:
            console.print("\n[bold red]Session interrupted. Goodbye![/bold red]")
            break
        except Exception as e:
            console.print(f"[bold red]Error: {str(e)}[/bold red]")

@click.command()
def main():
    """Start the interactive chat interface."""
    asyncio.run(chat_loop())

if __name__ == '__main__':
    main() 