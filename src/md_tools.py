from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict
import difflib
from pathlib import Path
import mistune
from mistune import create_markdown

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
        
        def process_node(node, depth=0):
            nonlocal current_section
            
            if node['type'] == 'heading':
                level = node['attrs']['level']
                title = ''.join(child['raw'] for child in node['children'] if child['type'] == 'text')
                
                # Count lines in the heading
                heading_lines = title.count('\n') + 1
                start_line = self._current_line
                self._current_line += heading_lines
                
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
            
            elif current_section and node['type'] == 'text':
                # Update section content and end line
                text = node['raw']
                current_section.content += text + '\n'
                # Update line count
                new_lines = text.count('\n') + 1
                self._current_line += new_lines
                current_section.end_line = self._current_line - 1
            
            # Process children
            for child in node.get('children', []):
                process_node(child, depth + 1)
        
        # Process the AST
        for node in ast[0]:
            process_node(node)
        
        return sections
    
    def get_section_by_title(self, content: str, title: str) -> Optional[Section]:
        """Get a section by its title."""
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
    
    def get_section_by_line(self, content: str, line_number: int) -> Optional[Section]:
        """Get a section that contains the given line number."""
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

class DiffGenerator:
    """Generates unified diffs for markdown sections."""
    
    @staticmethod
    def generate_diff(original_content: str, section: Section, modified_section_content: str, file_path: Path) -> str:
        """Generate a unified diff for a section, but at the file level.
        
        Args:
            original_content: The complete original file content
            section: The section being modified
            modified_section_content: The new content for the section
            file_path: Path to the file being modified
        """
        # Split the original content into lines
        lines = original_content.splitlines()
        
        # Create the modified content by replacing the section
        modified_lines = lines.copy()
        # Replace the section content (from start_line to end_line)
        modified_lines[section.start_line-1:section.end_line] = modified_section_content.splitlines()
        
        # Generate the diff
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
    def write_html_diff_to_file(html_diff: str, output_path: Path) -> None:
        """Write an HTML diff to a file."""
        with open(output_path, 'w') as f:
            f.write(html_diff)
    
    @staticmethod
    def print_terminal_diff(original_content: str, section: Section, modified_section_content: str, file_path: Path) -> None:
        """Print a colored diff to the terminal, showing the entire section.
        
        Args:
            original_content: The complete original file content
            section: The section being modified
            modified_section_content: The new content for the section
            file_path: Path to the file being modified
        """
        # Get the section's lines
        lines = original_content.splitlines()
        start_idx = max(0, section.start_line - 1)
        end_idx = min(len(lines), section.end_line)
        
        # Get the original section content
        original_section = lines[start_idx:end_idx]
        
        # Create the modified section content
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