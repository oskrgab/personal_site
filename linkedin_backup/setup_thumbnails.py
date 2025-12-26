#!/usr/bin/env python3
"""
Rename attachment images to thumbnails for Congo theme preview support.
"""

import os
import shutil
from pathlib import Path


def setup_thumbnails(blog_dir):
    """Rename attachment.jpg files to thumbnail.jpg."""
    blog_path = Path(blog_dir)

    renamed = 0
    skipped = 0

    # Find all attachment images
    for attachment in blog_path.glob("*/attachment.jpg"):
        folder = attachment.parent
        thumbnail = folder / "thumbnail.jpg"

        if thumbnail.exists():
            print(f"⏭️  Already exists: {folder.name}/thumbnail.jpg")
            skipped += 1
            continue

        try:
            # Rename attachment.jpg to thumbnail.jpg
            shutil.move(str(attachment), str(thumbnail))
            print(f"✅ Renamed: {folder.name}/attachment.jpg -> thumbnail.jpg")
            renamed += 1
        except Exception as e:
            print(f"❌ Error in {folder.name}: {e}")

    # Also check for .png files
    for attachment in blog_path.glob("*/attachment.png"):
        folder = attachment.parent
        thumbnail = folder / "thumbnail.png"

        if thumbnail.exists():
            print(f"⏭️  Already exists: {folder.name}/thumbnail.png")
            skipped += 1
            continue

        try:
            shutil.move(str(attachment), str(thumbnail))
            print(f"✅ Renamed: {folder.name}/attachment.png -> thumbnail.png")
            renamed += 1
        except Exception as e:
            print(f"❌ Error in {folder.name}: {e}")

    print(f"\n{'='*60}")
    print(f"Renamed: {renamed} images")
    print(f"Skipped: {skipped} images")
    print(f"{'='*60}")


if __name__ == '__main__':
    blog_dir = '/Users/oscarcortez/Documents/code/others/personal_site/content/blog'
    print("Setting up thumbnails for image previews...\n")
    setup_thumbnails(blog_dir)
