#!/usr/bin/env python3
"""
Analyze tag distribution from blog_tags_mapping.json
"""

import json
from collections import Counter


def analyze_tags(mapping_file):
    """Analyze tag distribution."""

    with open(mapping_file, 'r') as f:
        tag_mapping = json.load(f)

    # Count all tags
    all_tags = []
    for tags in tag_mapping.values():
        all_tags.extend(tags)

    tag_counts = Counter(all_tags)

    print("=" * 70)
    print("BLOG TAG ANALYSIS")
    print("=" * 70)
    print(f"\nTotal blog posts: {len(tag_mapping)}")
    print(f"Total unique tags: {len(tag_counts)}")
    print(f"Total tag assignments: {len(all_tags)}")
    print(f"Average tags per post: {len(all_tags)/len(tag_mapping):.1f}")

    print("\n" + "=" * 70)
    print("TOP 20 MOST USED TAGS")
    print("=" * 70)

    for i, (tag, count) in enumerate(tag_counts.most_common(20), 1):
        percentage = (count / len(tag_mapping)) * 100
        bar = "█" * int(count / 2)
        print(f"{i:2d}. {tag:25s} {count:3d} posts ({percentage:5.1f}%) {bar}")

    print("\n" + "=" * 70)
    print("ALL TAGS (Alphabetically)")
    print("=" * 70)

    for tag in sorted(tag_counts.keys()):
        count = tag_counts[tag]
        print(f"  • {tag:30s} ({count:3d} posts)")

    print("\n" + "=" * 70)
    print("TAG CATEGORIES")
    print("=" * 70)

    categories = {
        "Languages & Libraries": ["python", "rust", "numpy", "pandas", "scipy", "sympy"],
        "Topics": ["machine-learning", "data-science", "statistics", "bayesian-statistics",
                   "linear-algebra", "optimization", "time-series", "data-visualization"],
        "Tools & Platforms": ["excel", "git", "ide", "dev-containers", "cloud", "web-development"],
        "Content Type": ["tutorial", "opinion", "tips", "code-challenge", "beginner-friendly"],
        "Industry": ["oil-and-gas", "formulaml"],
        "AI & Automation": ["ai", "ai-tools", "chatgpt", "automation"],
        "Other": ["career-advice", "best-practices", "programming", "oop", "type-hints",
                  "units", "performance", "mobile", "personal", "announcement", "general", "history", "podcast"]
    }

    for category, tags in categories.items():
        print(f"\n{category}:")
        category_tags = {tag: tag_counts[tag] for tag in tags if tag in tag_counts}
        for tag in sorted(category_tags.keys(), key=lambda x: category_tags[x], reverse=True):
            print(f"  • {tag:30s} ({category_tags[tag]:3d} posts)")


if __name__ == '__main__':
    mapping_file = '/Users/oscarcortez/Documents/code/others/personal_site/blog_tags_mapping.json'
    analyze_tags(mapping_file)
