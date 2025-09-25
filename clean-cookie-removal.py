#!/usr/bin/env python3

"""
Surgical Cookie Consent Removal Script
Carefully removes cookie consent code while preserving file structure
"""

import os
import re
import sys
from pathlib import Path

# Configuration
target_directory = "."
backup_extension = ".backup"

def create_backup(file_path):
    """Create a backup of the original file"""
    backup_path = f"{file_path}{backup_extension}"
    with open(file_path, 'r', encoding='utf-8') as original:
        with open(backup_path, 'w', encoding='utf-8') as backup:
            backup.write(original.read())
    return backup_path

def remove_cookie_consent_html(content):
    """Remove cookie consent HTML elements"""
    # Remove cookie consent div blocks
    patterns_to_remove = [
        # Cookie consent divs and containers
        r'<div[^>]*id=["\']cookieConsent["\'][^>]*>.*?</div>\s*',
        r'<div[^>]*class=["\'][^"\']*cookie[^"\']*["\'][^>]*>.*?</div>\s*',

        # Cookie popup elements
        r'<div[^>]*cookie-consent[^>]*>.*?</div>\s*',
        r'<div[^>]*cookie-popup[^>]*>.*?</div>\s*',
    ]

    for pattern in patterns_to_remove:
        content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)

    return content

def remove_cookie_consent_css(content):
    """Remove cookie consent CSS rules"""
    patterns_to_remove = [
        # CSS rules for cookie consent
        r'\.cookie-consent\s*{[^}]*}\s*',
        r'\.cookie-hidden\s*{[^}]*}\s*',
        r'\.cookie-popup\s*{[^}]*}\s*',
        r'\.cookie-content\s*{[^}]*}\s*',
        r'\.cookie-text\s*{[^}]*}\s*',
        r'\.cookie-buttons\s*{[^}]*}\s*',
        r'\.cookie-button\s*{[^}]*}\s*',
        r'\.accept-all\s*{[^}]*}\s*',
        r'\.reject-all\s*{[^}]*}\s*',

        # Media queries for cookie consent
        r'@media[^{]*{\s*\.cookie[^}]*{[^}]*}\s*[^}]*}',
    ]

    for pattern in patterns_to_remove:
        content = re.sub(pattern, '', content, flags=re.MULTILINE | re.IGNORECASE)

    return content

def remove_cookie_consent_javascript(content):
    """Remove cookie consent JavaScript code"""
    patterns_to_remove = [
        # Function definitions
        r'function\s+acceptCookies\s*\([^)]*\)\s*{[^}]*(?:{[^}]*}[^}]*)*}\s*',
        r'function\s+rejectCookies\s*\([^)]*\)\s*{[^}]*(?:{[^}]*}[^}]*)*}\s*',
        r'function\s+acceptAllCookies\s*\([^)]*\)\s*{[^}]*(?:{[^}]*}[^}]*)*}\s*',
        r'function\s+rejectAllCookies\s*\([^)]*\)\s*{[^}]*(?:{[^}]*}[^}]*)*}\s*',
        r'function\s+checkCookieConsent\s*\([^)]*\)\s*{[^}]*(?:{[^}]*}[^}]*)*}\s*',
        r'function\s+hideCookiePopup\s*\([^)]*\)\s*{[^}]*(?:{[^}]*}[^}]*)*}\s*',
        r'function\s+showCookiePopup\s*\([^)]*\)\s*{[^}]*(?:{[^}]*}[^}]*)*}\s*',

        # Cookie consent IIFE blocks
        r'\(function\s*\(\)\s*{\s*["\']use strict["\'];.*?cookie.*?}\)\(\);\s*',

        # Event listeners for cookie consent
        r'popup\.addEventListener\(["\']click["\'],\s*acceptCookies\);\s*',
        r'window\.addEventListener\(["\']DOMContentLoaded["\'],\s*checkCookieConsent\);\s*',

        # Variable assignments
        r'window\.acceptAllCookies\s*=\s*acceptAllCookies;\s*',
        r'window\.rejectAllCookies\s*=\s*rejectAllCookies;\s*',

        # Comments about cookie consent
        r'//.*[Cc]ookie.*consent.*\n',
        r'/\*.*[Cc]ookie.*consent.*\*/\s*',
    ]

    for pattern in patterns_to_remove:
        old_content = content
        content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
        if old_content != content:
            print("  - Removed JavaScript pattern")

    return content

def clean_empty_script_tags(content):
    """Remove empty script tags after cleanup"""
    # Remove script tags that are now empty or only contain whitespace
    content = re.sub(r'<script[^>]*>\s*</script>\s*', '', content, flags=re.MULTILINE)
    return content

def process_html_file(file_path):
    """Process a single HTML file to remove cookie consent code"""
    print(f"Processing: {file_path}")

    try:
        # Create backup
        backup_path = create_backup(file_path)
        print(f"  - Created backup: {backup_path}")

        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_size = len(content)

        # Apply removal functions
        content = remove_cookie_consent_html(content)
        content = remove_cookie_consent_css(content)
        content = remove_cookie_consent_javascript(content)
        content = clean_empty_script_tags(content)

        # Clean up extra whitespace and empty lines
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)  # Remove excessive empty lines
        content = re.sub(r'[ \t]+\n', '\n', content)  # Remove trailing spaces

        new_size = len(content)
        reduction = original_size - new_size

        if reduction > 0:
            # Write cleaned content back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  - Cleaned {reduction} characters of cookie code")
        else:
            print("  - No cookie consent code found")
            # Remove unnecessary backup if no changes
            os.remove(backup_path)

    except Exception as e:
        print(f"  - Error processing {file_path}: {e}")
        # Restore from backup if it exists
        backup_path = f"{file_path}{backup_extension}"
        if os.path.exists(backup_path):
            os.rename(backup_path, file_path)
            print(f"  - Restored from backup due to error")

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
    print("Starting Surgical Cookie Consent Removal")
    print("=" * 50)

    # Find all HTML files
    html_files = find_html_files(target_directory)
    print(f"Found {len(html_files)} HTML files to process")
    print()

    processed_count = 0
    cleaned_count = 0

    for file_path in html_files:
        try:
            # Check if file has cookie consent code before processing
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if any(keyword in content.lower() for keyword in ['cookie', 'acceptcookies', 'rejectcookies', 'cookieconsent']):
                process_html_file(file_path)
                cleaned_count += 1
            else:
                print(f"Skipping: {file_path} (no cookie code detected)")

            processed_count += 1

        except Exception as e:
            print(f"Error with {file_path}: {e}")

    print()
    print("=" * 50)
    print(f"Surgical cookie removal complete!")
    print(f"Processed: {processed_count} files")
    print(f"Cleaned: {cleaned_count} files")
    print(f"Backups created for all modified files (.backup extension)")
    print()
    print("Next steps:")
    print("1. Test the website to ensure it still works")
    print("2. Implement new global cookie consent system")
    print("3. Remove backup files once satisfied with results")

if __name__ == "__main__":
    main()