#!/usr/bin/env python3
"""
Script to check navigation completeness in HTML files
"""
import os
import re
from pathlib import Path

def check_navigation_elements(file_path):
    """Check if file has complete navigation structure"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return {"error": "Could not read file"}

    checks = {
        "logo": bool(re.search(r'🚀.*ShopifyAppAuthority', content)),
        "best_apps": bool(re.search(r'Best Apps|Best Tools', content)),
        "categories": bool(re.search(r'App Categories|Categories.*dropdown', content)),
        "quick_faqs": bool(re.search(r'Quick FAQs', content)),
        "by_store_size": bool(re.search(r'By Store Size', content)),
        "disclosure": bool(re.search(r'Disclosure.*href.*affiliate', content)),
        "dropdown_structure": bool(re.search(r'dropdown-content', content)),
        "categories_dropdown_content": bool(re.search(r'Email Marketing.*Conversion.*Reviews.*Customer Service.*CRM.*Analytics.*Free Apps', content, re.DOTALL)),
        "faqs_dropdown_content": bool(re.search(r'Email Marketing FAQ.*Analytics.*Attribution FAQ.*CRM.*Sales FAQ', content, re.DOTALL)),
        "store_size_dropdown_content": bool(re.search(r'Small Stores.*Medium Stores.*Enterprise', content, re.DOTALL))
    }

    return checks

def main():
    base_dir = Path('C:/Projects/Shopifyappauthority-site')
    html_files = list(base_dir.glob('**/*.html'))

    print(f"Analyzing {len(html_files)} HTML files for navigation completeness...\n")

    missing_components = []
    complete_navigation = []

    for file_path in html_files:
        if 'MASTER_NAVIGATION_TEMPLATE.html' in str(file_path):
            continue

        result = check_navigation_elements(file_path)
        if "error" in result:
            continue

        # Count missing elements
        missing_elements = [key for key, value in result.items() if not value]

        if missing_elements:
            missing_components.append({
                'file': str(file_path.relative_to(base_dir)),
                'missing': missing_elements,
                'missing_count': len(missing_elements)
            })
        else:
            complete_navigation.append(str(file_path.relative_to(base_dir)))

    print(f"=== FILES WITH COMPLETE NAVIGATION ({len(complete_navigation)}) ===")
    for file in sorted(complete_navigation):
        print(f"[COMPLETE] {file}")

    print(f"\n=== FILES WITH MISSING NAVIGATION COMPONENTS ({len(missing_components)}) ===")

    # Sort by number of missing components (most problems first)
    missing_components.sort(key=lambda x: x['missing_count'], reverse=True)

    for item in missing_components:
        print(f"\n[MISSING] {item['file']} (missing {item['missing_count']} components):")
        for missing in item['missing']:
            print(f"  - {missing}")

if __name__ == "__main__":
    main()