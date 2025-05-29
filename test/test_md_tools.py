from drdemo.md_tools import MarkdownSectionParser, Section

def test_parse_sections():
    # Arrange
    parser = MarkdownSectionParser()
    markdown = """# Main Title
## Section 1
Content of section 1
## Section 2
Content of section 2
"""
    
    # Act
    sections = parser.parse_sections(markdown)
    
    # Assert
    assert len(sections) == 1  # One main section
    assert sections[0].title == "Main Title"
    assert len(sections[0].children) == 2  # Two subsections
    assert sections[0].children[0].title == "Section 1"
    assert sections[0].children[1].title == "Section 2"

def test_section_line_numbers():
    # Arrange
    parser = MarkdownSectionParser()
    markdown = """# Main Title
First line of main section
Second line of main section

## Section 1
Content of section 1
More content

## Section 2
Final content
"""
    
    # Act
    sections = parser.parse_sections(markdown)
    
    # Assert
    main_section = sections[0]
    assert main_section.start_line == 1  # Starts at first line
    assert main_section.end_line == 4    # Ends before Section 1
    
    section1 = main_section.children[0]
    assert section1.start_line == 5      # Starts at Section 1
    assert section1.end_line == 8        # Ends before Section 2
    
    section2 = main_section.children[1]
    assert section2.start_line == 10
    assert section2.end_line == 10 