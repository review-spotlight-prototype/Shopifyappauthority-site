#!/usr/bin/env python3
"""
Add Global Cookie Consent System
Adds consistent cookie consent implementation to all HTML files
"""

import os
import re
import glob

def add_cookie_consent_to_file(file_path):
    """Add the global cookie consent system to a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Check if cookie consent is already added
        if 'cookie-consent.css' in content and 'cookie-consent.js' in content:
            return False

        # Find the head section to add CSS
        css_link = '<link rel="stylesheet" href="/assets/cookie-consent.css">'
        if css_link not in content:
            head_pattern = r'(<head[^>]*>)'
            if re.search(head_pattern, content, re.IGNORECASE):
                content = re.sub(
                    head_pattern,
                    r'\1\n    ' + css_link,
                    content,
                    flags=re.IGNORECASE
                )

        # Find the body end to add JavaScript
        js_script = '<script src="/assets/cookie-consent.js"></script>'
        if js_script not in content:
            body_end_pattern = r'(</body>)'
            if re.search(body_end_pattern, content, re.IGNORECASE):
                content = re.sub(
                    body_end_pattern,
                    '    ' + js_script + '\n' + r'\1',
                    content,
                    flags=re.IGNORECASE
                )

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
    """Add global cookie consent to all HTML files"""
    print("Adding global cookie consent system...")

    # Find all HTML files
    html_files = glob.glob("**/*.html", recursive=True)

    modified_files = []

    for file_path in html_files:
        # Skip template files
        if 'TEMPLATE' in file_path.upper():
            continue

        print(f"Processing: {file_path}")
        if add_cookie_consent_to_file(file_path):
            modified_files.append(file_path)

    print(f"\nGlobal cookie consent implementation complete!")
    print(f"Files processed: {len(html_files)}")
    print(f"Files modified: {len(modified_files)}")

    if modified_files:
        print("\nModified files:")
        for file_path in modified_files:
            print(f"  - {file_path}")

    return len(modified_files)

if __name__ == "__main__":
    main()