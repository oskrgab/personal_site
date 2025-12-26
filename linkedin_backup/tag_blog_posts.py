#!/usr/bin/env python3
"""
Script to automatically assign tags to blog posts based on content analysis.
"""

import os
import re
from pathlib import Path
from typing import List, Set


def is_date_folder(folder_name):
    """Check if folder name matches date-title pattern."""
    return bool(re.match(r'^\d{4}-\d{2}-\d{2}-', folder_name))


# Define tag keywords - when these words appear, suggest these tags
TAG_KEYWORDS = {
    'python': ['python', 'pythonic', 'py', 'pip', 'conda', 'anaconda', 'pypi'],
    'machine learning': ['machine learning', 'ml model', 'regression', 'classification',
                         'random forest', 'neural network', 'training', 'prediction',
                         'supervised', 'unsupervised', 'overfitting', 'underfitting'],
    'data science': ['data science', 'data analysis', 'analytics', 'dataset', 'data-driven'],
    'pandas': ['pandas', 'dataframe', 'pd.', 'series'],
    'numpy': ['numpy', 'np.', 'array'],
    'statistics': ['statistics', 'statistical', 'probability', 'distribution',
                   'bayesian', 'frequentist', 'hypothesis', 'p-value'],
    'excel': ['excel', 'spreadsheet', 'xlsx', 'workbook'],
    'programming': ['programming', 'coding', 'developer', 'software', 'code'],
    'web development': ['web app', 'flask', 'django', 'dash', 'fastapi', 'html', 'css', 'javascript'],
    'data visualization': ['visualization', 'plotting', 'chart', 'graph', 'matplotlib',
                           'seaborn', 'plotly', 'd3'],
    'oil and gas': ['oil', 'gas', 'petroleum', 'reservoir', 'drilling', 'production forecast',
                    'well', 'decline curve'],
    'automation': ['automation', 'automate', 'automated', 'scripting'],
    'career': ['career', 'job', 'interview', 'resume', 'networking'],
    'tutorial': ['tutorial', 'how to', 'guide', 'step by step', 'walkthrough'],
    'rust': ['rust', 'rustlang', 'cargo'],
    'git': ['git', 'github', 'version control', 'commit', 'branch', 'merge'],
    'docker': ['docker', 'container', 'containerization'],
    'sql': ['sql', 'database', 'query', 'sqlite', 'postgresql', 'mysql'],
    'time series': ['time series', 'forecasting', 'arima', 'sarimax', 'temporal'],
    'best practices': ['best practice', 'clean code', 'code quality', 'refactoring'],
    'ai': ['ai', 'artificial intelligence', 'chatgpt', 'gpt', 'llm', 'claude'],
    'testing': ['testing', 'test', 'pytest', 'unittest', 'tdd'],
    'performance': ['performance', 'optimization', 'speed', 'efficiency', 'benchmark'],
    'beginners': ['beginner', 'getting started', 'introduction', 'basics', 'fundamentals'],
    'linear algebra': ['linear algebra', 'matrix', 'vector', 'eigenvalue'],
    'scipy': ['scipy', 'scientific computing'],
    'cloud': ['cloud', 'aws', 'azure', 'gcp', 'deployment'],
    'remote work': ['remote work', 'work from home', 'wfh'],
    'jupyter': ['jupyter', 'notebook', 'ipynb'],
    'vscode': ['vscode', 'vs code', 'visual studio code'],
    'pycharm': ['pycharm'],
    'linear programming': ['linear programming', 'optimization', 'objective function'],
    'enum': ['enum', 'enumeration'],
    'type hints': ['type hint', 'typing', 'annotation'],
    'formulas': ['formula', 'equation', 'mathematical'],
    'units': ['units', 'measurement', 'conversion'],
    'dev containers': ['dev container', 'devcontainer'],
    'chatgpt': ['chatgpt', 'gpt-4', 'openai'],
    'mcp': ['mcp', 'model context protocol'],
}

# Specific patterns to detect
PATTERNS = {
    'code challenge': r'(code challenge|puzzle|quiz)',
    'opinion': r'(i think|in my opinion|my favorite|i believe|i\'m falling for)',
    'tips': r'(tip|trick|hack|pitfall|mistake)',
}


def extract_content(file_path: Path) -> tuple[str, str, str]:
    """Extract title, description, and body content from markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract front matter
    parts = content.split('---', 2)
    if len(parts) < 3:
        return '', '', ''

    front_matter = parts[1]
    body = parts[2].strip()

    # Extract title
    title_match = re.search(r'title:\s*["\']?([^"\']+)["\']?', front_matter)
    title = title_match.group(1) if title_match else ''

    # Extract description
    desc_match = re.search(r'description:\s*["\']?([^"\']+)["\']?', front_matter)
    description = desc_match.group(1) if desc_match else ''

    return title.lower(), description.lower(), body.lower()


def suggest_tags(title: str, description: str, body: str) -> Set[str]:
    """Suggest tags based on content analysis."""
    suggested_tags = set()

    # Combine all text for analysis
    all_text = f"{title} {description} {body}"

    # Check for keyword matches
    for tag, keywords in TAG_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in all_text:
                suggested_tags.add(tag)
                break  # Found one keyword for this tag, move to next tag

    # Check for specific patterns
    for tag, pattern in PATTERNS.items():
        if re.search(pattern, all_text, re.IGNORECASE):
            suggested_tags.add(tag)

    return suggested_tags


def get_current_tags(file_path: Path) -> List[str]:
    """Extract current tags from the front matter."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    parts = content.split('---', 2)
    if len(parts) < 3:
        return []

    front_matter = parts[1]

    # Look for tags or topics field
    tags_match = re.search(r'(tags|topics):\s*\[(.*?)\]', front_matter, re.DOTALL)
    if tags_match:
        tags_str = tags_match.group(2)
        # Extract quoted strings
        tags = re.findall(r'["\']([^"\']+)["\']', tags_str)
        return tags

    return []


def update_tags(file_path: Path, new_tags: List[str]) -> bool:
    """Update the tags in the front matter."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"  ⚠️  Invalid front matter format")
        return False

    front_matter = parts[1]
    body = parts[2]

    # Format tags as YAML list
    tags_str = ', '.join([f'"{tag}"' for tag in sorted(new_tags)])
    tags_line = f'tags: [{tags_str}]'

    # Check if tags/topics already exist
    if re.search(r'(tags|topics):', front_matter):
        # Replace existing tags/topics
        front_matter = re.sub(
            r'(tags|topics):\s*\[.*?\]',
            tags_line,
            front_matter,
            flags=re.DOTALL
        )
    else:
        # Add tags after description or at the end
        if 'description:' in front_matter:
            # Find description line and add tags after it
            lines = front_matter.split('\n')
            new_lines = []
            for i, line in enumerate(lines):
                new_lines.append(line)
                if line.strip().startswith('description:'):
                    new_lines.append(tags_line)
            front_matter = '\n'.join(new_lines)
        else:
            # Add at the end of front matter
            front_matter = front_matter.rstrip() + f'\n{tags_line}\n'

    # Reconstruct the file
    new_content = f"---{front_matter}---{body}"

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True


def process_blog_posts(blog_dir: str, dry_run: bool = False):
    """Process all blog posts and assign tags."""
    blog_path = Path(blog_dir)

    if not blog_path.exists():
        print(f"Error: Blog directory not found: {blog_dir}")
        return

    processed = 0
    updated = 0
    skipped = 0

    # Collect all folders first
    folders = [f for f in sorted(blog_path.iterdir()) if f.is_dir() and is_date_folder(f.name)]

    print(f"Found {len(folders)} blog posts to process\n")

    for folder in folders:
        folder_name = folder.name
        index_file = folder / 'index.md'

        if not index_file.exists():
            print(f"⚠️  No index.md in {folder_name}")
            continue

        try:
            # Extract content
            title, description, body = extract_content(index_file)

            # Get current tags
            current_tags = get_current_tags(index_file)

            # Suggest new tags
            suggested_tags = suggest_tags(title, description, body)

            # Combine with existing tags (keep existing ones)
            all_tags = set(current_tags) | suggested_tags

            if not all_tags:
                print(f"⏭️  No tags for: {folder_name}")
                skipped += 1
                processed += 1
                continue

            # Convert to sorted list
            final_tags = sorted(all_tags)

            # Check if tags changed
            if set(current_tags) == set(final_tags):
                print(f"⏭️  No change: {folder_name}")
                skipped += 1
            else:
                if dry_run:
                    print(f"🔍 Would update {folder_name}")
                    print(f"   Current: {current_tags}")
                    print(f"   New: {final_tags}")
                else:
                    # Update the file
                    if update_tags(index_file, final_tags):
                        print(f"✅ Updated: {folder_name}")
                        print(f"   Tags: {final_tags}")
                        updated += 1
                    else:
                        print(f"❌ Failed: {folder_name}")

            processed += 1

        except Exception as e:
            print(f"❌ Error processing {folder_name}: {e}")

    print(f"\n{'='*60}")
    print(f"Processed: {processed} blog posts")
    print(f"Updated: {updated} blog posts")
    print(f"Skipped (no changes): {skipped} blog posts")
    print(f"{'='*60}")


if __name__ == '__main__':
    import sys

    blog_dir = '/Users/oscarcortez/Documents/code/others/personal_site/content/blog'

    # Check for dry-run flag
    dry_run = '--dry-run' in sys.argv

    if dry_run:
        print("🔍 DRY RUN MODE - No files will be modified\n")

    print(f"Analyzing and tagging blog posts in: {blog_dir}\n")
    process_blog_posts(blog_dir, dry_run=dry_run)
