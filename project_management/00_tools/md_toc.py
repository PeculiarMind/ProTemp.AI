#!/usr/bin/env python3
"""
Markdown Table of Contents Generator

This script generates a table of contents for markdown files by extracting
heading elements and creating navigatable links.

Usage:
    python md_toc.py <markdown_file> [options]

Options:
    --insert        Insert TOC into the file after the first heading
    --update        Update existing TOC in the file (same as --insert)
    --output FILE   Write TOC to a specific file
    --max-level N   Maximum heading level to include (default: 6)
    --min-level N   Minimum heading level to include (default: 1)
"""

import re
import sys
import argparse
from pathlib import Path


def slugify(text):
    """
    Convert heading text to GitHub-compatible anchor link.
    
    Args:
        text: The heading text to convert
        
    Returns:
        A URL-safe anchor string
    """
    # Remove markdown formatting (bold, italic, code, links)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # Italic
    text = re.sub(r'`([^`]+)`', r'\1', text)        # Inline code
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # Links
    
    # Convert to lowercase and replace spaces with hyphens
    slug = text.lower().strip()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    
    return slug


def extract_headings(content, min_level=1, max_level=6):
    """
    Extract headings from markdown content.
    
    Args:
        content: The markdown file content
        min_level: Minimum heading level to include
        max_level: Maximum heading level to include
        
    Returns:
        List of tuples (level, text, anchor)
    """
    headings = []
    lines = content.split('\n')
    
    for line in lines:
        # Match ATX-style headings (# Heading)
        match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            
            # Skip if outside level range
            if level < min_level or level > max_level:
                continue
            
            anchor = slugify(text)
            headings.append((level, text, anchor))
    
    return headings


def generate_toc(headings, min_level=None):
    """
    Generate table of contents from headings.
    
    Args:
        headings: List of tuples (level, text, anchor)
        min_level: Minimum level for indentation calculation
        
    Returns:
        String containing the TOC in markdown format
    """
    if not headings:
        return "**Table of Contents**\n\nNo headings found.\n"
    
    # Determine base level for indentation
    if min_level is None:
        min_level = min(h[0] for h in headings)
    
    toc_lines = ["**Table of Contents**", ""]
    
    for level, text, anchor in headings:
        indent = "  " * (level - min_level)
        toc_line = f"{indent}- [{text}](#{anchor})"
        toc_lines.append(toc_line)
    
    return "\n".join(toc_lines) + "\n"


def has_toc(content):
    """
    Check if content already has a TOC.
    
    Args:
        content: Markdown file content
        
    Returns:
        True if TOC exists, False otherwise
    """
    return '**Table of Contents**' in content or '## Table of Contents' in content


def find_toc_boundaries(lines):
    """
    Find the start and end indices of an existing TOC.
    
    Args:
        lines: List of content lines
        
    Returns:
        Tuple of (start_index, end_index) or (None, None) if no TOC found
    """
    toc_start = None
    toc_end = None
    
    for i, line in enumerate(lines):
        if '**Table of Contents**' in line or '## Table of Contents' in line:
            toc_start = i
            # Skip blank lines immediately after TOC header
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            
            # Find the end of TOC (next heading or non-list content)
            while j < len(lines):
                stripped = lines[j].strip()
                # End of TOC if we hit a heading
                if stripped.startswith('#'):
                    toc_end = j
                    break
                # End of TOC if we hit non-list, non-blank content
                if stripped and not stripped.startswith('-') and not stripped.startswith('*'):
                    toc_end = j
                    break
                j += 1
            
            if toc_end is None:
                toc_end = len(lines)
            break
    
    return toc_start, toc_end


def insert_toc_in_content(content, toc):
    """
    Insert TOC into markdown content after the first heading.
    Replaces existing TOC if found.
    
    Args:
        content: Original markdown content
        toc: Generated table of contents
        
    Returns:
        Updated content with TOC inserted
    """
    lines = content.split('\n')
    
    # Remove existing TOC if present
    toc_start, toc_end = find_toc_boundaries(lines)
    
    if toc_start is not None:
        lines = lines[:toc_start] + lines[toc_end:]
    
    # Find position after first heading to insert TOC
    insert_pos = None
    for i, line in enumerate(lines):
        if re.match(r'^#\s+', line.strip()):
            insert_pos = i + 1
            break
    
    if insert_pos is None:
        # No heading found, insert at the beginning
        insert_pos = 0
    
    # Insert TOC with blank lines
    toc_lines = [''] + toc.rstrip().split('\n') + ['']
    lines = lines[:insert_pos] + toc_lines + lines[insert_pos:]
    
    return '\n'.join(lines)


def main():
    """Main function to handle CLI arguments and generate TOC."""
    parser = argparse.ArgumentParser(
        description='Generate table of contents for markdown files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('file', help='Markdown file to process')
    parser.add_argument('--insert', action='store_true',
                        help='Insert TOC into the file after the first heading')
    parser.add_argument('--update', action='store_true',
                        help='Update existing TOC in the file (same as --insert)')
    parser.add_argument('--output', '-o', help='Write TOC to specific file')
    parser.add_argument('--max-level', type=int, default=6,
                        help='Maximum heading level to include (default: 6)')
    parser.add_argument('--min-level', type=int, default=1,
                        help='Minimum heading level to include (default: 1)')
    
    args = parser.parse_args()
    
    # Read the markdown file
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File '{args.file}' not found.", file=sys.stderr)
        sys.exit(1)
    
    content = file_path.read_text(encoding='utf-8')
    
    # Extract headings and generate TOC
    headings = extract_headings(content, args.min_level, args.max_level)
    toc = generate_toc(headings, args.min_level)
    
    # Handle output
    if args.insert or args.update:
        # Check if TOC already exists
        toc_exists = has_toc(content)
        
        # Insert or update TOC in the file
        updated_content = insert_toc_in_content(content, toc)
        file_path.write_text(updated_content, encoding='utf-8')
        
        if toc_exists:
            print(f"TOC updated in {args.file}")
        else:
            print(f"TOC inserted into {args.file}")
    elif args.output:
        # Write to output file
        output_path = Path(args.output)
        output_path.write_text(toc, encoding='utf-8')
        print(f"TOC written to {args.output}")
    else:
        # Print to stdout
        print(toc)


if __name__ == '__main__':
    main()
