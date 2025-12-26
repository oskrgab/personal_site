#!/usr/bin/env python3
"""
Script to fix blog post formatting issues.
Removes quotes from content lines and replaces "" with actual empty lines.
"""

import os
import re
from pathlib import Path


def is_date_folder(folder_name):
    """Check if folder name matches date-title pattern (not numbered like 1_, 2_, etc)."""
    # Pattern: starts with YYYY-MM-DD
    return bool(re.match(r'^\d{4}-\d{2}-\d{2}-', folder_name))


def fix_content_formatting(content):
    """Fix the formatting of blog post content."""
    lines = content.split('\n')
    fixed_lines = []
    in_frontmatter = False
    frontmatter_count = 0

    for line in lines:
        # Track frontmatter boundaries (between --- markers)
        if line.strip() == '---':
            frontmatter_count += 1
            fixed_lines.append(line)
            if frontmatter_count == 1:
                in_frontmatter = True
            elif frontmatter_count == 2:
                in_frontmatter = False
            continue

        # Keep frontmatter lines as-is
        if in_frontmatter or frontmatter_count < 2:
            fixed_lines.append(line)
            continue

        # Process content after frontmatter
        stripped = line.strip()

        # Empty quoted string becomes blank line
        if stripped == '""':
            fixed_lines.append('')
        # Single quote on its own line - remove it
        elif stripped == '"':
            fixed_lines.append('')
        # Line wrapped in quotes - remove them
        elif stripped.startswith('"') and stripped.endswith('"') and len(stripped) > 1:
            # Remove leading and trailing quotes
            unquoted = stripped[1:-1]
            fixed_lines.append(unquoted)
        # Line with trailing quote only - remove it
        elif stripped.endswith('"') and not stripped.startswith('"'):
            # Remove trailing quote
            fixed_lines.append(stripped[:-1])
        # Keep other lines as-is
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def process_blog_posts(blog_dir):
    """Process all blog posts in date-titled folders."""
    blog_path = Path(blog_dir)

    if not blog_path.exists():
        print(f"Error: Blog directory not found: {blog_dir}")
        return

    processed = 0
    fixed = 0

    # Iterate through all subdirectories
    for folder in sorted(blog_path.iterdir()):
        if not folder.is_dir():
            continue

        folder_name = folder.name

        # Skip numbered folders (1_, 2_, etc)
        if not is_date_folder(folder_name):
            continue

        # Look for index.md file
        index_file = folder / 'index.md'
        if not index_file.exists():
            print(f"⚠️  No index.md in {folder_name}")
            continue

        # Read the file
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                original_content = f.read()

            # Fix the formatting
            fixed_content = fix_content_formatting(original_content)

            # Only write if content changed
            if original_content != fixed_content:
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                print(f"✅ Fixed: {folder_name}")
                fixed += 1
            else:
                print(f"⏭️  No changes: {folder_name}")

            processed += 1

        except Exception as e:
            print(f"❌ Error processing {folder_name}: {e}")

    print(f"\n{'='*60}")
    print(f"Processed: {processed} blog posts")
    print(f"Fixed: {fixed} blog posts")
    print(f"{'='*60}")


if __name__ == '__main__':
    blog_dir = '/Users/oscarcortez/Documents/code/others/personal_site/content/blog'
    print(f"Fixing blog post formatting in: {blog_dir}\n")
    process_blog_posts(blog_dir)
