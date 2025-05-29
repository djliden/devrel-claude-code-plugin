from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict
import difflib
from pathlib import Path
import mistune
from mistune import create_markdown
import patch
import tempfile
import shutil

@dataclass
class Section:
    """Represents a section in a markdown document."""
    title: str
    content: str
    start_line: int
    end_line: int
    level: int  # Header level (1-6)
    children: List['Section']  # Nested sections

class MarkdownSectionParser:
    """Parser for retrieving sections from markdown documents using AST."""
    
    def __init__(self):
        self.markdown = create_markdown(renderer='ast')
        self._current_line = 1
    
    def parse_sections(self, content: str) -> List[Section]:
        """Parse markdown content and return a list of sections using AST."""
        self._current_line = 1
        ast = self.markdown.parse(content)
        sections = []
        current_section = None
        section_stack = []
        
        def get_text_from_node(node):
            """Helper function to extract text from a node and its children."""
            if node['type'] == 'text':
                return node['raw']
            elif node['type'] in ['codespan', 'block_code']:
                return node['raw']
            elif 'children' in node:
                # Join children with newlines to preserve markdown formatting
                return '\n'.join(get_text_from_node(child) for child in node['children'])
            return ''

        def process_node(node, depth=0):
            nonlocal current_section
            
            if node['type'] == 'heading':
                level = node['attrs']['level']
                title = get_text_from_node(node)
                
                # Count lines in the heading
                heading_lines = title.count('\n') + 1
                start_line = self._current_line
                self._current_line += heading_lines
                
                # If we have a current section, end it before starting a new one
                if current_section:
                    current_section.end_line = start_line - 1
                
                # Create new section
                new_section = Section(
                    title=title,
                    content='',
                    start_line=start_line,
                    end_line=start_line,
                    level=level,
                    children=[]
                )
                
                # Handle section hierarchy
                while section_stack and section_stack[-1].level >= level:
                    section_stack.pop()
                
                if section_stack:
                    section_stack[-1].children.append(new_section)
                else:
                    sections.append(new_section)
                
                section_stack.append(new_section)
                current_section = new_section
            
            elif current_section:
                if node['type'] == 'blank_line':
                    current_section.content += '\n'
                    self._current_line += 1
                    current_section.end_line = self._current_line - 1
                
                elif node['type'] == 'paragraph':
                    text = get_text_from_node(node)
                    # Don't add an extra newline since get_text_from_node already adds them
                    current_section.content += text
                    new_lines = text.count('\n')
                    self._current_line += new_lines
                    current_section.end_line = self._current_line - 1
                
                elif node['type'] == 'block_code':
                    # Handle code blocks with their markers
                    marker = node['marker']
                    info = node['attrs'].get('info', '')
                    code = node['raw']
                    current_section.content += f"{marker}{info}\n{code}{marker}\n"
                    new_lines = code.count('\n') + 3  # +3 for the markers and info
                    self._current_line += new_lines
                    current_section.end_line = self._current_line - 1
                
                elif node['type'] == 'list':
                    # Handle lists
                    for item in node['children']:
                        if item['type'] == 'list_item':
                            # Get the bullet or number
                            bullet = node['bullet']
                            if node['attrs'].get('ordered'):
                                start = node['attrs'].get('start', 1)
                                prefix = f"{start}. "
                            else:
                                prefix = f"{bullet} "
                            
                            # Get the item content
                            item_text = get_text_from_node(item)
                            current_section.content += prefix + item_text + '\n'
                            new_lines = item_text.count('\n') + 1
                            self._current_line += new_lines
                            current_section.end_line = self._current_line - 1
                
                elif node['type'] == 'codespan':
                    # Handle inline code
                    code = node['raw']
                    current_section.content += f"`{code}`"
                    new_lines = code.count('\n')
                    self._current_line += new_lines
                    current_section.end_line = self._current_line - 1
                
                elif node['type'] == 'link':
                    # Handle links
                    text = get_text_from_node(node)
                    url = node['attrs']['url']
                    current_section.content += f"[{text}]({url})"
                    new_lines = text.count('\n')
                    self._current_line += new_lines
                    current_section.end_line = self._current_line - 1
            
            # Process children
            for child in node.get('children', []):
                process_node(child, depth + 1)
        
        # Process the AST
        for node in ast[0]:
            process_node(node)
        
        return sections

    def parse_file(self, file_path: Path) -> List[Section]:
        """Parse a markdown file and return a list of sections."""
        with open(file_path, 'r') as f:
            content = f.read()
        return self.parse_sections(content)
    
    def get_section_by_title(self, content: str, title: str) -> Optional[Section]:
        """Get a section by its title from a string content."""
        def find_section(sections: List[Section], target_title: str) -> Optional[Section]:
            for section in sections:
                if section.title.lower() == target_title.lower():
                    return section
                if section.children:
                    result = find_section(section.children, target_title)
                    if result:
                        return result
            return None
        
        sections = self.parse_sections(content)
        return find_section(sections, title)

    def get_section_by_title_from_file(self, file_path: Path, title: str) -> Optional[Section]:
        """Get a section by its title from a file."""
        with open(file_path, 'r') as f:
            content = f.read()
        return self.get_section_by_title(content, title)
    
    def get_section_by_line(self, content: str, line_number: int) -> Optional[Section]:
        """Get a section that contains the given line number from a string content."""
        def find_section(sections: List[Section], target_line: int) -> Optional[Section]:
            for section in sections:
                if section.start_line <= target_line <= section.end_line:
                    # Check children first
                    if section.children:
                        result = find_section(section.children, target_line)
                        if result:
                            return result
                    return section
            return None
        
        sections = self.parse_sections(content)
        return find_section(sections, line_number)

    def get_section_by_line_from_file(self, file_path: Path, line_number: int) -> Optional[Section]:
        """Get a section that contains the given line number from a file."""
        with open(file_path, 'r') as f:
            content = f.read()
        return self.get_section_by_line(content, line_number)

class DiffGenerator:
    """Generates unified diffs for markdown sections."""
    
    @staticmethod
    def _get_section_boundaries(lines: List[str], start_idx: int) -> Tuple[int, int]:
        """Get the start and end indices for a section.
        
        Args:
            lines: List of lines from the file
            start_idx: Starting index of the section
            
        Returns:
            Tuple of (start_idx, end_idx) for the section content
        """
        # Find where the next section starts by looking for the next heading
        next_section_start = len(lines)
        for i in range(start_idx + 1, len(lines)):
            if lines[i].startswith('##'):
                next_section_start = i
                break
        return start_idx, next_section_start
    
    @staticmethod
    def _prepare_diff_content(original_content: str, section: Section, modified_section_content: str) -> Tuple[List[str], List[str]]:
        """Prepare the original and modified content for diffing.
        
        Args:
            original_content: The complete original file content
            section: The section being modified
            modified_section_content: The new content for the section
            
        Returns:
            Tuple of (original_lines, modified_lines)
        """
        # Split the original content into lines
        lines = original_content.splitlines()
        
        # Create the modified content by replacing the section
        modified_lines = lines.copy()
        
        # Get the section's lines
        start_idx = section.start_line - 1  # Convert to 0-based index
        
        # Get section boundaries
        start_idx, next_section_start = DiffGenerator._get_section_boundaries(lines, start_idx)
        
        # Replace just the content between the heading and the next section
        modified_lines[start_idx:next_section_start] = modified_section_content.splitlines()
        
        return lines, modified_lines
    
    @staticmethod
    def generate_diff(original_content: str, section: Section, modified_section_content: str, file_path: Path) -> str:
        """Generate a unified diff for a section, but at the file level."""
        lines, modified_lines = DiffGenerator._prepare_diff_content(original_content, section, modified_section_content)
        
        # Generate the diff with proper line numbers
        diff = difflib.unified_diff(
            lines,
            modified_lines,
            fromfile=str(file_path),
            tofile=str(file_path),
            lineterm='',
            n=3  # Context lines
        )
        return '\n'.join(diff)

    @staticmethod
    def generate_diff_from_files(original_file: Path, section: Section, modified_section_content: str) -> str:
        """Generate a unified diff for a section from files.
        
        Args:
            original_file: Path to the original file
            section: The section being modified
            modified_section_content: The new content for the section
        """
        with open(original_file, 'r') as f:
            original_content = f.read()
        return DiffGenerator.generate_diff(original_content, section, modified_section_content, original_file)
    
    @staticmethod
    def write_diff_to_file(diff: str, output_path: Path) -> None:
        """Write a diff to a file."""
        with open(output_path, 'w') as f:
            f.write(diff)
    
    @staticmethod
    def generate_html_diff(original_content: str, section: Section, modified_section_content: str, file_path: Path) -> str:
        """Generate an HTML diff view of the changes, showing the entire section.
        
        Args:
            original_content: The complete original file content
            section: The section being modified
            modified_section_content: The new content for the section
            file_path: Path to the file being modified
        """
        # Get the section's lines with some context
        lines = original_content.splitlines()
        start_idx = max(0, section.start_line - 1)
        end_idx = min(len(lines), section.end_line)
        
        # Get the original section content
        original_section = lines[start_idx:end_idx]
        
        # Create the modified section content
        modified_section = modified_section_content.splitlines()
        
        # Generate HTML diff
        html_diff = difflib.HtmlDiff(wrapcolumn=80)
        return html_diff.make_file(
            original_section,
            modified_section,
            f"{file_path} (original)",
            f"{file_path} (modified)",
            context=True,
            numlines=0  # Show all lines
        )

    @staticmethod
    def generate_html_diff_from_files(original_file: Path, section: Section, modified_section_content: str) -> str:
        """Generate an HTML diff view of the changes from files.
        
        Args:
            original_file: Path to the original file
            section: The section being modified
            modified_section_content: The new content for the section
        """
        with open(original_file, 'r') as f:
            original_content = f.read()
        return DiffGenerator.generate_html_diff(original_content, section, modified_section_content, original_file)
    
    @staticmethod
    def write_html_diff_to_file(html_diff: str, output_path: Path) -> None:
        """Write an HTML diff to a file."""
        with open(output_path, 'w') as f:
            f.write(html_diff)
    
    @staticmethod
    def print_terminal_diff(original_content: str, section: Section, modified_section_content: str, file_path: Path) -> None:
        """Print a colored diff to the terminal, showing the entire section."""
        # Get the section's lines
        lines = original_content.splitlines()
        start_idx = section.start_line - 1  # Convert to 0-based index
        start_idx, next_section_start = DiffGenerator._get_section_boundaries(lines, start_idx)
        
        # Get the original section content
        original_section = lines[start_idx:next_section_start]
        
        # Get the modified section content
        modified_section = modified_section_content.splitlines()
        
        print(f"\nSection: {section.title}")
        print("=" * 80)
        
        # Generate and print the diff
        for line in difflib.ndiff(original_section, modified_section):
            if line.startswith('+ '):
                print(f"\033[92m{line}\033[0m")  # Green for additions
            elif line.startswith('- '):
                print(f"\033[91m{line}\033[0m")  # Red for deletions
            elif line.startswith('? '):
                continue  # Skip the hint lines
            else:
                print(line)
        
        print("=" * 80)

    @staticmethod
    def print_terminal_diff_from_files(original_file: Path, section: Section, modified_section_content: str) -> None:
        """Print a colored diff to the terminal from files.
        
        Args:
            original_file: Path to the original file
            section: The section being modified
            modified_section_content: The new content for the section
        """
        with open(original_file, 'r') as f:
            original_content = f.read()
        DiffGenerator.print_terminal_diff(original_content, section, modified_section_content, original_file)

class PatchApplier:
    """Applies patch files to markdown documents."""
    
    @staticmethod
    def apply_patch(file_path: Path, patch_path: Path) -> bool:
        """Apply a patch file to a markdown document.
        
        Args:
            file_path: Path to the markdown file to patch
            patch_path: Path to the patch file
            
        Returns:
            bool: True if patch was applied successfully, False otherwise
        """
        try:
            patcher = patch.fromfile(str(patch_path))
            if not patcher:
                raise ValueError("Invalid patch file")
            
            with open(file_path, 'r') as f:
                content = f.read()
            
            patched_content = patcher.apply(content)
            if patched_content is None:
                raise ValueError("Failed to apply patch")
            
            with open(file_path, 'w') as f:
                f.write(patched_content)
            
            return True
            
        except Exception as e:
            print(f"Error applying patch: {str(e)}")
            return False 