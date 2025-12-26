#!/usr/bin/env python3
"""
Apply curated tags from blog_tags_mapping.json to all blog posts.
"""

import json
import re
from pathlib import Path


def update_tags_in_file(file_path: Path, new_tags: list) -> bool:
    """Update the tags in a blog post file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"  ⚠️  Invalid front matter format")
        return False

    front_matter = parts[1]
    body = parts[2]

    # Format topics as YAML list
    topics_str = ', '.join([f'"{tag}"' for tag in new_tags])
    topics_line = f'topics: [{topics_str}]'

    # Replace existing tags/topics
    if re.search(r'(tags|topics):', front_matter):
        front_matter = re.sub(
            r'(tags|topics):\s*\[.*?\]',
            topics_line,
            front_matter,
            flags=re.DOTALL
        )
    else:
        # Add topics after description or at the end
        if 'description:' in front_matter:
            lines = front_matter.split('\n')
            new_lines = []
            for line in lines:
                new_lines.append(line)
                if line.strip().startswith('description:'):
                    new_lines.append(topics_line)
            front_matter = '\n'.join(new_lines)
        else:
            front_matter = front_matter.rstrip() + f'\n{topics_line}\n'

    # Reconstruct file
    new_content = f"---{front_matter}---{body}"

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True


def apply_tags(mapping_file: str, blog_dir: str):
    """Apply tags from mapping file to all blog posts."""

    # Load tag mapping
    with open(mapping_file, 'r', encoding='utf-8') as f:
        tag_mapping = json.load(f)

    blog_path = Path(blog_dir)
    updated = 0
    skipped = 0
    errors = 0

    print(f"Applying curated tags to blog posts...\n")

    for folder_name, tags in tag_mapping.items():
        folder = blog_path / folder_name
        index_file = folder / 'index.md'

        if not index_file.exists():
            print(f"⚠️  File not found: {folder_name}")
            skipped += 1
            continue

        try:
            if update_tags_in_file(index_file, tags):
                print(f"✅ {folder_name}")
                print(f"   Tags: {tags}")
                updated += 1
            else:
                print(f"❌ Failed: {folder_name}")
                errors += 1
        except Exception as e:
            print(f"❌ Error: {folder_name} - {e}")
            errors += 1

    print(f"\n{'='*60}")
    print(f"Updated: {updated} posts")
    print(f"Skipped: {skipped} posts")
    print(f"Errors: {errors} posts")
    print(f"{'='*60}")


if __name__ == '__main__':
    mapping_file = '/Users/oscarcortez/Documents/code/others/personal_site/blog_tags_mapping.json'
    blog_dir = '/Users/oscarcortez/Documents/code/others/personal_site/content/blog'

    apply_tags(mapping_file, blog_dir)
