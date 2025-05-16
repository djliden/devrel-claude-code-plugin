from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, Container
from textual.widgets import Header, Footer, Input, Button, Static, TextArea
from textual.binding import Binding
from pathlib import Path
from .context import load_context, save_context, get_context_file

class TutorialGenerator(App):
    """A TUI for generating tutorials and guides using AI."""
    
    BINDINGS = [
        ("ctrl+s", "submit", "Submit"),
    ]
    
    def __init__(self, file_path: Path):
        super().__init__()
        self.current_file = file_path
        self.context = load_context(file_path)
        self.file_content = self.current_file.read_text() if self.current_file.exists() else ""
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=True)
        
        with Container():
            # File name input
            with Horizontal(id="file-name-area"):
                yield Static("File name:", classes="label")
                yield Input(value=self.current_file.stem, id="file-name-input")
                yield Button("Save", id="save-name-button")
            
            # Main chat area
            with Vertical(id="chat-area"):
                yield Static("Welcome to the Tutorial Generator! Let's create an outline for your tutorial.", id="welcome-message")
                yield TextArea(id="chat-history", read_only=True)
            
            # Input area
            with Horizontal(id="input-area"):
                yield Input(value="Type your message here...", id="user-input")
                yield Button("Send", id="send-button")
            
            # Outline preview
            with Vertical(id="outline-area"):
                yield Static("Current Outline", classes="section-header")
                yield TextArea(self.file_content, id="outline-preview", read_only=True)
            
            # Context area
            with Vertical(id="context-area"):
                yield Static("Context", classes="section-header")
                context_text = "\n".join(self.context["context"]) if self.context["context"] else "Add URLs, files, or text here..."
                yield TextArea(text=context_text, id="context-input")
            
            # Options area
            with Vertical(id="options-area"):
                yield Static("Options", classes="section-header")
                yield Button(
                    "Enable Web Search" if not self.context["options"]["web_search"] else "Disable Web Search",
                    id="web-search-toggle"
                )
        
        yield Footer()

    def on_mount(self) -> None:
        """Set up the app when it starts."""
        self.title = f"Tutorial Generator - {self.current_file.name}"
        self.sub_title = "AI-Powered Tutorial Creation"
        
        # Add initial AI message
        chat_history = self.query_one("#chat-history", TextArea)
        chat_history.insert("AI: I'll help you create an outline for your tutorial. What would you like to write about?\n")

    def action_submit(self) -> None:
        """Handle the submit action."""
        input_widget = self.query_one("#user-input", Input)
        if input_widget.value:
            chat_history = self.query_one("#chat-history", TextArea)
            chat_history.insert(f"\nYou: {input_widget.value}\n")
            
            # TODO: Process with AI and update outline
            # For now, just echo back
            chat_history.insert(f"AI: I understand you want to write about: {input_widget.value}\n")
            
            input_widget.value = ""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "save-name-button":
            new_name = self.query_one("#file-name-input", Input).value
            if new_name:
                new_path = Path(f"{new_name}.md")
                if new_path != self.current_file:
                    # Rename the file
                    self.current_file.rename(new_path)
                    self.current_file = new_path
                    self.title = f"Tutorial Generator - {new_path.name}"
                    
                    # Update context file
                    old_context_file = get_context_file(self.current_file)
                    if old_context_file.exists():
                        old_context_file.unlink()
                    self.context["file_path"] = str(new_path)
                    save_context(new_path, self.context)
        
        elif event.button.id == "web-search-toggle":
            self.context["options"]["web_search"] = not self.context["options"]["web_search"]
            event.button.label = "Enable Web Search" if not self.context["options"]["web_search"] else "Disable Web Search"
            save_context(self.current_file, self.context)

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        """Handle text area changes."""
        if event.text_area.id == "context-input":
            self.context["context"] = [line for line in event.value.split("\n") if line.strip()]
            save_context(self.current_file, self.context)

if __name__ == "__main__":
    app = TutorialGenerator(Path("untitled.md"))
    app.run()
