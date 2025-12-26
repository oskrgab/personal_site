#!/usr/bin/env python3
"""
Script to read all blog posts and prepare them for manual tagging analysis.
Outputs a JSON file with post contents for review.
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict


def is_date_folder(folder_name):
    """Check if folder name matches date-title pattern."""
    return bool(re.match(r'^\d{4}-\d{2}-\d{2}-', folder_name))


def extract_post_info(file_path: Path) -> Dict:
    """Extract all relevant information from a blog post."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract front matter and body
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None

    front_matter = parts[1]
    body = parts[2].strip()

    # Extract title
    title_match = re.search(r'title:\s*["\']?([^"\']+)["\']?', front_matter)
    title = title_match.group(1) if title_match else ''

    # Extract description
    desc_match = re.search(r'description:\s*["\']?([^"\']+)["\']?', front_matter)
    description = desc_match.group(1) if desc_match else ''

    # Extract date
    date_match = re.search(r'date:\s*([^\n]+)', front_matter)
    date = date_match.group(1).strip() if date_match else ''

    # Clean body - remove images, links, keep text
    body_clean = re.sub(r'!\[.*?\]\(.*?\)', '', body)
    body_clean = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', body_clean)
    body_clean = re.sub(r'{{<.*?>}}', '', body_clean)

    # Get first ~500 chars of body for preview
    body_preview = body_clean[:800].strip()

    return {
        'folder': file_path.parent.name,
        'title': title,
        'description': description,
        'date': date,
        'body_preview': body_preview,
        'full_body': body_clean,
        'file_path': str(file_path)
    }


def collect_all_posts(blog_dir: str) -> List[Dict]:
    """Collect information from all blog posts."""
    blog_path = Path(blog_dir)
    posts = []

    folders = [f for f in sorted(blog_path.iterdir())
               if f.is_dir() and is_date_folder(f.name)]

    for folder in folders:
        index_file = folder / 'index.md'
        if not index_file.exists():
            continue

        try:
            post_info = extract_post_info(index_file)
            if post_info:
                posts.append(post_info)
        except Exception as e:
            print(f"Error processing {folder.name}: {e}")

    return posts


if __name__ == '__main__':
    blog_dir = '/Users/oscarcortez/Documents/code/others/personal_site/content/blog'

    print("Collecting all blog posts...")
    posts = collect_all_posts(blog_dir)

    print(f"\nFound {len(posts)} blog posts")
    print("\nFirst 5 posts:")
    for i, post in enumerate(posts[:5]):
        print(f"\n{i+1}. {post['title']}")
        print(f"   Date: {post['date']}")
        print(f"   Preview: {post['body_preview'][:100]}...")

    # Save to JSON for analysis
    output_file = 'blog_posts_analysis.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    print(f"\n\nSaved all posts to {output_file}")
