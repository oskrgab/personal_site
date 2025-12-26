#!/usr/bin/env python3
"""
Fix trailing quotes in blog post titles.
"""

import re
from pathlib import Path


def is_date_folder(folder_name):
    """Check if folder name matches date-title pattern."""
    return bool(re.match(r'^\d{4}-\d{2}-\d{2}-', folder_name))


def fix_title_quotes(file_path: Path) -> bool:
    """Remove trailing quotes from title and description."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    parts = content.split('---', 2)
    if len(parts) < 3:
        return False

    front_matter = parts[1]
    body = parts[2]

    # Track if any changes were made
    changed = False

    # Fix title - remove trailing backslash-quote pattern
    # Pattern matches: title: "text\""
    title_pattern = r'title:\s*"([^"]*)\\"\"'
    title_match = re.search(title_pattern, front_matter)
    if title_match:
        title_content = title_match.group(1)
        new_title_line = f'title: "{title_content}"'
        front_matter = re.sub(
            title_pattern,
            new_title_line,
            front_matter,
            count=1
        )
        changed = True

    # Fix description - remove trailing backslash-quote pattern
    # Pattern matches: description: "text\""
    desc_pattern = r'description:\s*"([^"]*)\\"\"'
    desc_match = re.search(desc_pattern, front_matter)
    if desc_match:
        desc_content = desc_match.group(1)
        new_desc_line = f'description: "{desc_content}"'
        front_matter = re.sub(
            desc_pattern,
            new_desc_line,
            front_matter,
            count=1
        )
        changed = True

    if changed:
        # Reconstruct file
        new_content = f"---{front_matter}---{body}"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return changed


def fix_all_titles(blog_dir: str):
    """Fix titles in all blog posts."""
    blog_path = Path(blog_dir)

    fixed = 0
    skipped = 0

    folders = [f for f in sorted(blog_path.iterdir())
               if f.is_dir() and is_date_folder(f.name)]

    print(f"Checking {len(folders)} blog posts for title issues...\n")

    for folder in folders:
        index_file = folder / 'index.md'
        if not index_file.exists():
            continue

        try:
            if fix_title_quotes(index_file):
                print(f"✅ Fixed: {folder.name}")
                fixed += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"❌ Error in {folder.name}: {e}")

    print(f"\n{'='*60}")
    print(f"Fixed: {fixed} posts")
    print(f"No changes needed: {skipped} posts")
    print(f"{'='*60}")


if __name__ == '__main__':
    blog_dir = '/Users/oscarcortez/Documents/code/others/personal_site/content/blog'
    fix_all_titles(blog_dir)
