#!/usr/bin/env python3

"""
Favicon Update Script
Updates all favicon references to the new image URL across all HTML files
"""

import os
import re
import sys
from pathlib import Path

# Configuration
target_directory = "."
new_favicon_url = "https://imagedelivery.net/mYndgAUf_CYgFA1HoO_-GQ/43e7272a-fb53-44aa-f0f2-7656a83bc700/public"

def update_favicon_references(content):
    """Update favicon link references to the new URL"""
    # Pattern to match favicon link tags
    favicon_patterns = [
        r'<link[^>]*rel=["\']icon["\'][^>]*href=["\'][^"\']*["\'][^>]*>',
        r'<link[^>]*href=["\'][^"\']*["\'][^>]*rel=["\']icon["\'][^>]*>',
        r'<link[^>]*rel=["\']shortcut\s+icon["\'][^>]*href=["\'][^"\']*["\'][^>]*>',
        r'<link[^>]*href=["\'][^"\']*["\'][^>]*rel=["\']shortcut\s+icon["\'][^>]*>',
    ]

    updated = False

    for pattern in favicon_patterns:
        def replace_favicon(match):
            nonlocal updated
            link_tag = match.group(0)
            # Replace the href attribute with the new URL
            new_link = re.sub(
                r'href=["\'][^"\']*["\']',
                f'href="{new_favicon_url}"',
                link_tag
            )
            # Ensure the type attribute is set correctly
            if 'type=' not in new_link:
                new_link = new_link.replace(
                    'rel="icon"',
                    'rel="icon" type="image/png"'
                ).replace(
                    "rel='icon'",
                    "rel='icon' type='image/png'"
                )
            updated = True
            return new_link

        content = re.sub(pattern, replace_favicon, content, flags=re.IGNORECASE)

    return content, updated

def process_html_file(file_path):
    """Process a single HTML file to update favicon references"""
    print(f"Processing: {file_path}")

    try:
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update favicon references
        new_content, updated = update_favicon_references(content)

        if updated:
            # Write updated content back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  - Updated favicon reference")
            return True
        else:
            print(f"  - No favicon references found")
            return False

    except Exception as e:
        print(f"  - Error processing {file_path}: {e}")
        return False

def find_html_files(directory):
    """Find all HTML files in the directory"""
    html_files = []
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories and common non-content directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]

        for file in files:
            if file.endswith('.html') and not file.startswith('.'):
                html_files.append(os.path.join(root, file))

    return html_files

def main():
    """Main execution function"""
    print("Updating Favicon References")
    print("=" * 50)
    print(f"New favicon URL: {new_favicon_url}")
    print()

    # Find all HTML files
    html_files = find_html_files(target_directory)
    print(f"Found {len(html_files)} HTML files to process")
    print()

    processed_count = 0
    updated_count = 0

    for file_path in html_files:
        try:
            if process_html_file(file_path):
                updated_count += 1
            processed_count += 1

        except Exception as e:
            print(f"Error with {file_path}: {e}")

    print()
    print("=" * 50)
    print(f"Favicon update complete!")
    print(f"Processed: {processed_count} files")
    print(f"Updated: {updated_count} files")
    print(f"New favicon URL: {new_favicon_url}")

if __name__ == "__main__":
    main()