import os
import re
import glob
from collections import defaultdict

def audit_cookie_implementations():
    """Comprehensive audit of all cookie consent implementations."""

    # Find all HTML files
    html_files = []
    for pattern in ['*.html', '*/*.html', '*/*/*.html']:
        html_files.extend(glob.glob(pattern))

    # Exclude test files and backups
    html_files = [f for f in html_files if 'test-' not in f and '.backup' not in f and 'debug' not in f and 'audit' not in f]

    # Data structures to collect findings
    function_names = defaultdict(list)
    element_ids = defaultdict(list)
    class_names = defaultdict(list)
    implementations = defaultdict(list)

    print(f"Auditing {len(html_files)} HTML files...")
    print("="*80)

    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Skip files without cookie/consent references
            if 'cookie' not in content.lower() and 'consent' not in content.lower():
                continue

            print(f"\n[FILE] {filepath}")

            # 1. Function names
            cookie_functions = re.findall(r'function\s+([\w]+(?:Cookie|Consent)[\w]*)\s*\(', content, re.IGNORECASE)
            for func in cookie_functions:
                function_names[func].append(filepath)
                print(f"   [FUNCTION] {func}")

            # 2. Element IDs
            cookie_ids = re.findall(r'id=["\']([^"\']*(?:cookie|consent)[^"\']*)["\']', content, re.IGNORECASE)
            for elem_id in cookie_ids:
                element_ids[elem_id].append(filepath)
                print(f"   [ID] {elem_id}")

            # 3. Class names
            cookie_classes = re.findall(r'class=["\']([^"\']*(?:cookie|consent)[^"\']*)["\']', content, re.IGNORECASE)
            for class_name in cookie_classes:
                class_names[class_name].append(filepath)
                print(f"   [CLASS] {class_name}")

            # 4. onclick handlers
            onclick_handlers = re.findall(r'onclick=["\']([^"\']*(?:cookie|consent)[^"\']*)["\']', content, re.IGNORECASE)
            for handler in onclick_handlers:
                implementations[f"onclick: {handler}"].append(filepath)
                print(f"   [ONCLICK] {handler}")

            # 5. addEventListener patterns
            event_listeners = re.findall(r'addEventListener\(["\']([^"\']+)["\'],\s*([^,\)]+)', content)
            for event, handler in event_listeners:
                if 'cookie' in handler.lower() or 'consent' in handler.lower():
                    implementations[f"addEventListener: {event} -> {handler}"].append(filepath)
                    print(f"   [EVENT] {event} -> {handler}")

            # 6. localStorage usage
            localstorage_keys = re.findall(r'localStorage\.(?:getItem|setItem|removeItem)\(["\']([^"\']*(?:cookie|consent)[^"\']*)["\']', content, re.IGNORECASE)
            for key in localstorage_keys:
                implementations[f"localStorage: {key}"].append(filepath)
                print(f"   [STORAGE] {key}")

            # 7. CSS display/visibility patterns
            css_patterns = re.findall(r'\.style\.(?:display|visibility)\s*=\s*["\']([^"\']+)["\']', content)
            if css_patterns:
                print(f"   [CSS] {css_patterns}")

        except Exception as e:
            print(f"   [ERROR] {filepath}: {e}")

    # Summary report
    print("\n" + "="*80)
    print("SUMMARY REPORT")
    print("="*80)

    print(f"\n[FUNCTIONS] ({len(function_names)} unique):")
    for func, files in sorted(function_names.items()):
        print(f"   {func}: {len(files)} files")
        if len(files) <= 5:
            for f in files[:3]:
                print(f"      - {f}")
            if len(files) > 3:
                print(f"      - ... and {len(files)-3} more")

    print(f"\n[IDS] ({len(element_ids)} unique):")
    for elem_id, files in sorted(element_ids.items()):
        print(f"   {elem_id}: {len(files)} files")

    print(f"\n[CLASSES] ({len(class_names)} unique):")
    for class_name, files in sorted(class_names.items()):
        print(f"   {class_name}: {len(files)} files")

    print(f"\n[PATTERNS] ({len(implementations)} unique):")
    for pattern, files in sorted(implementations.items()):
        print(f"   {pattern}: {len(files)} files")
        if len(files) <= 3:
            for f in files:
                print(f"      - {f}")

    # Recommendations
    print(f"\n[RECOMMENDATIONS]:")
    print("   1. Standardize on single function names: acceptCookies() and rejectCookies()")
    print("   2. Use consistent element ID: cookieConsent")
    print("   3. Use consistent class names: cookie-consent, cookie-hidden")
    print("   4. Implement single global cookie consent script")
    print("   5. Remove all duplicate/conflicting implementations")

    total_files_with_cookies = len(set(
        [f for files in function_names.values() for f in files] +
        [f for files in element_ids.values() for f in files] +
        [f for files in class_names.values() for f in files] +
        [f for files in implementations.values() for f in files]
    ))

    print(f"\n[STATISTICS]:")
    print(f"   Total files with cookie/consent code: {total_files_with_cookies}")
    print(f"   Total HTML files scanned: {len(html_files)}")
    print(f"   Percentage with cookie code: {total_files_with_cookies/len(html_files)*100:.1f}%")

if __name__ == "__main__":
    audit_cookie_implementations()