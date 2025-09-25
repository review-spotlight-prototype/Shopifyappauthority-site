import os
import re
import glob

def completely_remove_cookie_code(filepath):
    """Completely remove ALL cookie consent code from HTML files."""

    # Read the file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    changes_made = []

    print(f"\n[PROCESSING] {filepath}")

    # 1. Remove all cookie-related HTML elements
    html_patterns = [
        # Cookie consent popups with various IDs
        r'<div\s+id=["\']cookieConsent["\'][^>]*>.*?</div>\s*(?=\n|\r|\s*<)',
        r'<div\s+id=["\']cookieBanner["\'][^>]*>.*?</div>\s*(?=\n|\r|\s*<)',
        # Any div with cookie/consent classes
        r'<div[^>]*class=["\'][^"\']*(?:cookie|consent)[^"\']*["\'][^>]*>.*?</div>\s*(?=\n|\r|\s*<)',
        # Comments about cookie consent
        r'<!--.*?[Cc]ookie.*?[Cc]onsent.*?-->',
        r'<!--.*?[Cc]onsent.*?[Cc]ookie.*?-->',
    ]

    for pattern in html_patterns:
        matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
        if matches:
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
            changes_made.append(f"Removed {len(matches)} cookie HTML elements")

    # 2. Remove all cookie-related CSS
    css_patterns = [
        # Cookie consent CSS blocks
        r'/\*[^*]*[Cc]ookie[^*]*[Cc]onsent[^*]*\*/.*?(?=\n\s*/\*|\n\s*[.#@]|\n\s*</style>|\n\s*$)',
        r'\.cookie-[^{]*\{[^}]*\}',
        r'\.consent-[^{]*\{[^}]*\}',
        r'#cookieConsent[^{]*\{[^}]*\}',
        r'#cookieBanner[^{]*\{[^}]*\}',
        # Cookie hidden class
        r'\.cookie-hidden\s*\{[^}]*\}',
    ]

    for pattern in css_patterns:
        matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
        if matches:
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
            changes_made.append(f"Removed {len(matches)} cookie CSS rules")

    # 3. Remove all cookie-related JavaScript functions
    js_function_patterns = [
        # Individual function removals
        r'function\s+(?:accept|reject|decline)(?:All)?Cookies?\s*\([^)]*\)\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',
        r'function\s+(?:hide|show)Cookie(?:Popup|Banner)\s*\([^)]*\)\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',
        r'function\s+checkCookieConsent\s*\([^)]*\)\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',
        r'function\s+showCookieBanner\s*\([^)]*\)\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',
        # Wrapper functions
        r'function\s+(?:acceptCookies|rejectCookies|declineCookies)\s*\([^)]*\)\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',
    ]

    for pattern in js_function_patterns:
        matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
        if matches:
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
            changes_made.append(f"Removed {len(matches)} cookie JavaScript functions")

    # 4. Remove cookie-related event listeners and scripts
    js_script_patterns = [
        # Event listeners for cookie functions
        r'document\.addEventListener\(["\'](?:DOMContentLoaded|click)["\'],\s*(?:checkCookieConsent|acceptCookies|rejectCookies)[^)]*\)[^;]*;?',
        r'window\.addEventListener\(["\'](?:DOMContentLoaded|load)["\'],\s*(?:checkCookieConsent|function[^}]*cookie[^}]*)[^)]*\)[^;]*;?',
        # Button event listeners
        r'(?:acceptBtn|rejectBtn|declineBtn)\.addEventListener\([^)]+\)[^;]*;?',
        # Cookie-related IIFEs and script blocks
        r'\(function\(\)\s*\{\s*["\']use strict["\'];[^}]*(?:cookie|consent)[^}]*\}\)\(\);?',
        # Simple click handlers
        r'// (?:Simple|Removed)[^\n]*(?:cookie|consent)[^\n]*\n',
    ]

    for pattern in js_script_patterns:
        matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
        if matches:
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
            changes_made.append(f"Removed {len(matches)} cookie JavaScript handlers")

    # 5. Remove cookie-related comments and cleanup
    comment_patterns = [
        r'//[^\n]*(?:[Cc]ookie|[Cc]onsent)[^\n]*\n?',
        r'/\*[^*]*(?:[Cc]ookie|[Cc]onsent)[^*]*\*/',
        # Empty script tags
        r'<script[^>]*>\s*</script>',
        # Multiple empty lines
        r'\\n\\s*\\n\\s*\\n',
    ]

    for pattern in comment_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            content = re.sub(pattern, lambda m: '\\n' if '\\n' in pattern else '', content, flags=re.IGNORECASE)
            changes_made.append(f"Cleaned up {len(matches)} cookie comments/whitespace")

    # 6. Clean up onclick handlers in HTML
    onclick_patterns = [
        r'onclick=["\'](?:accept|reject|decline)(?:All)?Cookies\(\)["\']',
    ]

    for pattern in onclick_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
            changes_made.append(f"Removed {len(matches)} onclick cookie handlers")

    # 7. Final cleanup - remove empty lines and fix spacing
    content = re.sub(r'\\n\\s*\\n\\s*\\n+', '\\n\\n', content)  # Multiple empty lines
    content = re.sub(r'\\s*\\n\\s*\\n\\s*</script>', '\\n</script>', content)  # Empty script tags
    content = re.sub(r'<script>\\s*</script>', '', content)  # Completely empty scripts

    # Only write if content changed
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        for change in changes_made:
            print(f"   - {change}")
        return True, changes_made

    return False, []

def main():
    """Remove ALL cookie consent code from all HTML files."""

    # Find all HTML files
    html_files = []
    for pattern in ['*.html', '*/*.html', '*/*/*.html']:
        html_files.extend(glob.glob(pattern))

    # Exclude test/temp files
    html_files = [f for f in html_files if not any(x in f.lower() for x in ['test-', '.backup', 'debug', 'audit', 'nuke-'])]

    print(f"NUCLEAR COOKIE CLEANUP - Processing {len(html_files)} files...")
    print("="*80)

    fixed_count = 0
    error_count = 0
    total_changes = []

    for filepath in html_files:
        try:
            fixed, changes = completely_remove_cookie_code(filepath)
            if fixed:
                fixed_count += 1
                total_changes.extend(changes)
        except Exception as e:
            print(f"   [ERROR] {filepath}: {e}")
            error_count += 1

    print("\\n" + "="*80)
    print("CLEANUP SUMMARY")
    print("="*80)
    print(f"Files processed: {len(html_files)}")
    print(f"Files cleaned: {fixed_count}")
    print(f"Files with errors: {error_count}")
    print(f"Files unchanged: {len(html_files) - fixed_count - error_count}")

    # Summary of changes
    change_summary = {}
    for change in total_changes:
        if change in change_summary:
            change_summary[change] += 1
        else:
            change_summary[change] = 1

    print(f"\\nCHANGES BREAKDOWN:")
    for change_type, count in sorted(change_summary.items()):
        print(f"   {change_type}: {count} files")

    print(f"\\nREADY FOR CLEAN REIMPLEMENTATION!")
    print("   Next steps:")
    print("   1. Create single, clean cookie consent system")
    print("   2. Add consistent HTML/CSS/JS to all pages")
    print("   3. Test thoroughly")
    print("   4. Deploy")

if __name__ == "__main__":
    main()