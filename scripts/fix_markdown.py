"""Auto-fix markdown issues: table spacing and list blank lines."""

import re
from pathlib import Path


def fix_table_spacing(content: str) -> str:
    """Fix table pipe spacing - add space around pipes."""
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Check if this is a table line (contains |)
        if '|' in line and not line.strip().startswith('```'):
            # Skip code blocks
            if line.strip().startswith('|') or re.search(r'\|.*\|', line):
                # Add spaces around pipes
                # First, normalize: remove multiple spaces and add single space
                parts = line.split('|')
                fixed_parts = []
                for i, part in enumerate(parts):
                    if i == 0 or i == len(parts) - 1:
                        # First and last parts (outside pipes)
                        fixed_parts.append(part)
                    else:
                        # Inner parts - ensure spaces on both sides
                        stripped = part.strip()
                        if stripped.startswith('-') and all(c in '-:' for c in stripped):
                            # This is a separator row
                            fixed_parts.append(f' {stripped} ')
                        elif stripped:
                            fixed_parts.append(f' {stripped} ')
                        else:
                            fixed_parts.append('   ')
                line = '|'.join(fixed_parts)
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)


def fix_list_spacing(content: str) -> str:
    """Add blank lines around lists."""
    lines = content.split('\n')
    fixed_lines = []
    in_code_block = False
    
    for i, line in enumerate(lines):
        # Track code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
        
        if not in_code_block:
            # Check if this is a list item
            is_list = bool(re.match(r'^(\s*)[-*+](?:\s|$)', line) or re.match(r'^(\s*)\d+\.(?:\s|$)', line))
            
            # Get previous line info
            prev_line = fixed_lines[-1] if fixed_lines else ''
            prev_is_list = bool(re.match(r'^(\s*)[-*+](?:\s|$)', prev_line) or re.match(r'^(\s*)\d+\.(?:\s|$)', prev_line))
            prev_is_blank = prev_line.strip() == ''
            prev_is_heading = prev_line.strip().startswith('#')
            
            # Add blank line before list if needed
            if is_list and not prev_is_list and not prev_is_blank and prev_line.strip():
                # Check if we need to add blank line
                if not prev_is_heading or not prev_is_blank:
                    fixed_lines.append('')
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)


def fix_heading_spacing(content: str) -> str:
    """Add blank lines after headings before lists."""
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        fixed_lines.append(line)
        
        # If this is a heading
        if line.strip().startswith('#') and not line.strip().startswith('```'):
            # Check if next line exists and is a list
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                is_next_list = bool(re.match(r'^(\s*)[-*+](?:\s|$)', next_line) or 
                                   re.match(r'^(\s*)\d+\.(?:\s|$)', next_line))
                is_next_blank = next_line.strip() == ''
                
                if is_next_list and not is_next_blank:
                    fixed_lines.append('')
    
    return '\n'.join(fixed_lines)


def fix_trailing_newline(content: str) -> str:
    """Ensure file ends with single newline."""
    return content.rstrip() + '\n'


def fix_markdown_file(filepath: Path) -> bool:
    """Fix all markdown issues in a file."""
    try:
        content = filepath.read_text(encoding='utf-8')
        original = content
        
        content = fix_table_spacing(content)
        content = fix_list_spacing(content)
        content = fix_heading_spacing(content)
        content = fix_trailing_newline(content)
        
        # Remove duplicate blank lines
        while '\n\n\n' in content:
            content = content.replace('\n\n\n', '\n\n')
        
        if content != original:
            filepath.write_text(content, encoding='utf-8')
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False


def main():
    """Fix all markdown files."""
    root = Path('.')
    
    # Find all markdown files
    md_files = list(root.glob('**/*.md'))
    
    # Exclude node_modules, .git, etc
    md_files = [f for f in md_files if not any(
        part.startswith('.') or part == 'node_modules' 
        for part in f.parts
    )]
    
    fixed_count = 0
    for filepath in md_files:
        if fix_markdown_file(filepath):
            print(f"Fixed: {filepath}")
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} of {len(md_files)} files")


if __name__ == "__main__":
    main()
