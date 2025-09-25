#!/usr/bin/env python3
"""
Surgical Cookie Consent Removal Script
Removes all existing cookie consent implementations while preserving other functionality
"""

import os
import re
import glob

def remove_cookie_consent_from_file(file_path):
    """Remove all cookie consent related code from a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Remove cookie consent HTML blocks
        # Pattern for cookie consent divs with various IDs and classes
        cookie_div_patterns = [
            r'<div[^>]*(?:id|class)[^>]*(?:cookie|Cookie)[^>]*>.*?</div>\s*',
            r'<div[^>]*(?:cookieConsent|cookieBanner|cookie-consent|cookie-banner)[^>]*>.*?</div>\s*',
            r'<!-- Cookie Consent -->.*?<!-- End Cookie Consent -->\s*',
            r'<!-- Cookie consent banner -->.*?<!-- /Cookie consent banner -->\s*',
        ]

        for pattern in cookie_div_patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)

        # Remove cookie consent CSS
        css_patterns = [
            r'\.cookie-consent\s*\{[^}]*\}',
            r'\.cookie-banner\s*\{[^}]*\}',
            r'\.cookieConsent\s*\{[^}]*\}',
            r'\.cookie-hidden\s*\{[^}]*\}',
            r'\.cookie-popup\s*\{[^}]*\}',
            r'#cookieConsent\s*\{[^}]*\}',
            r'#cookieBanner\s*\{[^}]*\}',
            r'/\*[^*]*cookie[^*]*\*/\s*[^{]*\{[^}]*\}',
        ]

        for pattern in css_patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)

        # Remove cookie consent JavaScript functions
        js_patterns = [
            r'function\s+(?:accept|reject|decline)(?:All)?Cookies?\s*\([^)]*\)\s*\{[^}]*\}',
            r'function\s+(?:show|hide)CookieConsent\s*\([^)]*\)\s*\{[^}]*\}',
            r'function\s+checkCookieConsent\s*\([^)]*\)\s*\{[^}]*\}',
            r'function\s+setCookieConsent\s*\([^)]*\)\s*\{[^}]*\}',
        ]

        for pattern in js_patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)

        # Remove localStorage cookie operations
        localStorage_patterns = [
            r'localStorage\.(?:setItem|getItem|removeItem)\s*\([^)]*["\']cookie[^)]*\)',
            r'localStorage\.(?:setItem|getItem|removeItem)\s*\([^)]*["\']cookieConsent[^)]*\)',
            r'localStorage\.(?:setItem|getItem|removeItem)\s*\([^)]*["\']gdpr[^)]*\)',
        ]

        for pattern in localStorage_patterns:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)

        # Remove cookie consent event listeners
        event_patterns = [
            r'document\.(?:getElementById|querySelector)\s*\([^)]*cookie[^)]*\)\.addEventListener[^;]*;',
            r'document\.addEventListener\s*\([^)]*function[^}]*cookie[^}]*\}[^;]*\);',
        ]

        for pattern in event_patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)

        # Clean up extra whitespace and empty lines
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        content = re.sub(r'^\s*$\n', '', content, flags=re.MULTILINE)

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
    """Remove cookie consent from all HTML files"""
    print("Starting surgical cookie consent removal...")

    # Find all HTML files
    html_files = glob.glob("**/*.html", recursive=True)

    modified_files = []

    for file_path in html_files:
        print(f"Processing: {file_path}")
        if remove_cookie_consent_from_file(file_path):
            modified_files.append(file_path)

    print(f"\nRemoval complete!")
    print(f"Files processed: {len(html_files)}")
    print(f"Files modified: {len(modified_files)}")

    if modified_files:
        print("\nModified files:")
        for file_path in modified_files:
            print(f"  - {file_path}")

    return len(modified_files)

if __name__ == "__main__":
    main()