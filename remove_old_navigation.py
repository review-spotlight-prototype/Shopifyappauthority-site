#!/usr/bin/env python3
"""
Remove old navigation CSS and elements that are conflicting with the global navigation
"""

import re
import os
from pathlib import Path

def remove_old_navigation_css(content):
    """Remove old navigation CSS using generic selectors"""

    # Remove header CSS block (generic header styles)
    header_css_pattern = r'header\s*\{[^}]*\}(?:\s*nav\s*\{[^}]*\})?(?:\s*\.logo\s*\{[^}]*\})?(?:\s*\.nav-links[^{]*\{[^}]*\})*(?:\s*\.nav-links\s*a[^{]*\{[^}]*\})*(?:\s*\.nav-links\s*a:hover[^{]*\{[^}]*\})*(?:\s*\.dropdown[^{]*\{[^}]*\})*(?:\s*\.dropdown[^{]*::after[^{]*\{[^}]*\})*(?:\s*\.dropdown-content[^{]*\{[^}]*\})*(?:\s*\.dropdown:hover\s*\.dropdown-content[^{]*\{[^}]*\})*(?:\s*\.dropdown-content\s*a[^{]*\{[^}]*\})*(?:\s*\.dropdown-content\s*a:hover[^{]*\{[^}]*\})*(?:\s*\.mobile-menu-toggle[^{]*\{[^}]*\})*(?:\s*@media[^{]*\{[^{}]*\{[^}]*\}[^{}]*\})*'

    # More targeted approach - remove blocks that start with specific selectors
    patterns_to_remove = [
        r'header\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',  # header styles
        r'nav\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',     # nav styles
        r'\.logo\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',  # logo styles (non site-header)
        r'\.nav-links\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', # nav-links styles
        r'\.nav-links\s+a\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', # nav links a styles
        r'\.nav-links\s+a:hover\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', # nav links hover
        r'\.dropdown\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', # dropdown styles
        r'\.dropdown\s*>\s*a::after\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', # dropdown arrows
        r'\.dropdown-content\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', # dropdown content
        r'\.dropdown:hover\s*\.dropdown-content\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', # dropdown hover
        r'\.dropdown-content\s+a\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', # dropdown links
        r'\.dropdown-content\s+a:hover\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', # dropdown link hover
        r'\.mobile-menu-toggle\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', # mobile toggle
    ]

    changes_made = 0
    for pattern in patterns_to_remove:
        matches = list(re.finditer(pattern, content, re.DOTALL))
        if matches:
            print(f"    Removing {len(matches)} old navigation CSS blocks")
            changes_made += len(matches)
            for match in reversed(matches):
                content = content[:match.start()] + content[match.end():]

    # Remove mobile responsive CSS for old navigation
    mobile_css_pattern = r'@media\s*\([^)]*max-width:\s*768px[^)]*\)[^{]*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    mobile_matches = list(re.finditer(mobile_css_pattern, content, re.DOTALL))
    if mobile_matches:
        # Only remove mobile CSS that contains old navigation selectors
        for match in reversed(mobile_matches):
            mobile_content = match.group()
            if any(selector in mobile_content for selector in ['nav {', '.nav-links', '.dropdown-content', 'header {']):
                print(f"    Removing old mobile navigation CSS")
                content = content[:match.start()] + content[match.end():]
                changes_made += 1

    if changes_made > 0:
        print(f"    Removed {changes_made} old navigation CSS elements")

    return content

def fix_file(file_path):
    """Fix a single file by removing old navigation"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        content = remove_old_navigation_css(original_content)

        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  [CLEANED] {file_path}")
            return True
        else:
            print(f"  [NO OLD NAV] {file_path}")
            return False

    except Exception as e:
        print(f"  [ERROR] {file_path}: {str(e)}")
        return False

def main():
    """Main function to remove old navigation from all HTML files"""
    base_dir = Path(".")

    print("Removing old navigation CSS that conflicts with global navigation...")

    # Find all HTML files
    html_files = list(base_dir.glob('**/*.html'))
    html_files = [f for f in html_files if 'MASTER_NAVIGATION_TEMPLATE.html' not in str(f)]
    html_files = [f for f in html_files if not any(part.startswith('.') for part in f.parts)]

    print(f"Checking {len(html_files)} HTML files for old navigation CSS")

    fixed_count = 0

    # Check specific problem files first
    priority_files = [
        Path('moosend-review/index.html'),
        Path('aweber-review/index.html'),
        Path('activecampaign-review/index.html'),
        Path('getresponse-review/index.html')
    ]

    print("\n=== PRIORITY FILES ===")
    for file_path in priority_files:
        if file_path.exists():
            print(f"\nProcessing PRIORITY: {file_path}...")
            if fix_file(file_path):
                fixed_count += 1
        else:
            print(f"Priority file not found: {file_path}")

    print("\n=== ALL OTHER FILES ===")
    for file_path in html_files:
        if file_path not in priority_files:
            print(f"\nProcessing: {file_path}...")
            if fix_file(file_path):
                fixed_count += 1

    print(f"\nRemoved old navigation CSS from {fixed_count} files")
    print("Global navigation should now be the only navigation system!")

if __name__ == "__main__":
    main()