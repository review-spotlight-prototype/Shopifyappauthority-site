#!/usr/bin/env python3
"""
Update all HTML files to use the new favicon with purple background
"""

import os
import re
import glob

def update_favicon_in_file(file_path):
    """Update favicon references in a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Replace the old favicon URL with the new local file
        old_favicon_url = 'https://imagedelivery.net/mYndgAUf_CYgFA1HoO_-GQ/43e7272a-fb53-44aa-f0f2-7656a83bc700/public'
        new_favicon_path = '/favicon-with-background.ico'

        # Update favicon link tags
        content = content.replace(old_favicon_url, new_favicon_path)

        # Also update any remaining favicon.ico references
        content = re.sub(r'href="/?favicon\.ico"', f'href="{new_favicon_path}"', content)

        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Update favicon in all HTML files"""
    print("Updating favicon references to use purple background version...")

    # Find all HTML files
    html_files = glob.glob("**/*.html", recursive=True)

    modified_files = []

    for file_path in html_files:
        print(f"Processing: {file_path}")
        if update_favicon_in_file(file_path):
            modified_files.append(file_path)

    print(f"\nFavicon update complete!")
    print(f"Files processed: {len(html_files)}")
    print(f"Files modified: {len(modified_files)}")

    if modified_files:
        print("\nModified files:")
        for file_path in modified_files[:10]:  # Show first 10
            print(f"  - {file_path}")
        if len(modified_files) > 10:
            print(f"  ... and {len(modified_files) - 10} more files")

    return len(modified_files)

if __name__ == "__main__":
    main()