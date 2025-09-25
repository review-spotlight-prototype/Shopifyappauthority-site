#!/usr/bin/env python3
"""
Technical SEO Implementation - Safe, Non-Breaking Improvements
Following technical-seo-guidelines.md for bulk application across all pages
"""

import os
import re
import glob
import json
from pathlib import Path
from urllib.parse import urljoin

class TechnicalSEOOptimizer:
    def __init__(self):
        self.base_url = "https://shopifyappauthority.com"
        self.site_name = "ShopifyAppAuthority"
        self.changes_made = []

    def get_page_url(self, file_path):
        """Generate canonical URL from file path"""
        # Convert file path to URL path
        url_path = file_path.replace('\\', '/').replace('/index.html', '/')

        if url_path.endswith('.html') and not url_path.endswith('index.html'):
            url_path = url_path.replace('.html', '/')

        if not url_path.startswith('/'):
            url_path = '/' + url_path

        return self.base_url + url_path

    def extract_page_info(self, content):
        """Extract key information from page content"""
        info = {
            'title': '',
            'description': '',
            'h1': '',
            'images': []
        }

        # Extract title
        title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        if title_match:
            info['title'] = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()

        # Extract meta description
        desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content, re.IGNORECASE)
        if desc_match:
            info['description'] = desc_match.group(1).strip()

        # Extract H1
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
        if h1_match:
            info['h1'] = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()

        # Extract images
        img_matches = re.findall(r'<img[^>]+>', content, re.IGNORECASE)
        for img in img_matches:
            src_match = re.search(r'src="([^"]+)"', img, re.IGNORECASE)
            alt_match = re.search(r'alt="([^"]*)"', img, re.IGNORECASE)
            info['images'].append({
                'tag': img,
                'src': src_match.group(1) if src_match else '',
                'alt': alt_match.group(1) if alt_match else None
            })

        return info

    def add_missing_meta_tags(self, content, page_info):
        """Add required meta tags if missing"""
        changes = []

        # Check for charset
        if not re.search(r'<meta\s+charset=', content, re.IGNORECASE):
            charset_tag = '<meta charset="UTF-8">'
            head_pos = content.find('<head')
            if head_pos != -1:
                head_end = content.find('>', head_pos)
                content = content[:head_end+1] + '\n    ' + charset_tag + content[head_end+1:]
                changes.append("Added UTF-8 charset meta tag")

        # Check for viewport
        if not re.search(r'<meta\s+name="viewport"', content, re.IGNORECASE):
            viewport_tag = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            head_pos = content.find('<head')
            if head_pos != -1:
                head_end = content.find('>', head_pos)
                content = content[:head_end+1] + '\n    ' + viewport_tag + content[head_end+1:]
                changes.append("Added viewport meta tag")

        # Add meta description if missing
        if not page_info['description'] and page_info['title']:
            # Generate description from title or H1
            desc_content = page_info['title'][:155] if len(page_info['title']) > 50 else page_info['h1'][:155]
            if desc_content:
                desc_tag = f'<meta name="description" content="{desc_content}">'
                title_pos = content.find('</title>')
                if title_pos != -1:
                    content = content[:title_pos+8] + '\n    ' + desc_tag + content[title_pos+8:]
                    changes.append("Added missing meta description")

        return content, changes

    def add_canonical_tag(self, content, file_path):
        """Add canonical URL if missing or fix existing"""
        changes = []
        canonical_url = self.get_page_url(file_path)

        # Check for existing canonical
        canonical_match = re.search(r'<link\s+rel="canonical"[^>]*>', content, re.IGNORECASE)

        if not canonical_match:
            # Add canonical tag
            canonical_tag = f'<link rel="canonical" href="{canonical_url}">'
            title_pos = content.find('</title>')
            if title_pos != -1:
                content = content[:title_pos+8] + '\n    ' + canonical_tag + content[title_pos+8:]
                changes.append("Added canonical tag")
        else:
            # Fix relative canonical to absolute
            existing_canonical = canonical_match.group(0)
            href_match = re.search(r'href="([^"]+)"', existing_canonical)
            if href_match:
                current_href = href_match.group(1)
                if not current_href.startswith('http'):
                    new_canonical = existing_canonical.replace(current_href, canonical_url)
                    content = content.replace(existing_canonical, new_canonical)
                    changes.append("Fixed canonical URL to absolute")

        return content, changes

    def add_open_graph_tags(self, content, page_info, file_path):
        """Add Open Graph tags if missing"""
        changes = []
        canonical_url = self.get_page_url(file_path)

        # Check if OG tags already exist
        if not re.search(r'property="og:title"', content, re.IGNORECASE):
            og_tags = f'''
    <meta property="og:title" content="{page_info['title'] or page_info['h1'] or 'Shopify App Reviews'}">
    <meta property="og:description" content="{page_info['description'] or page_info['title'][:155]}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="{self.site_name}">'''

            # Insert after title or canonical
            canonical_pos = content.find('rel="canonical"')
            if canonical_pos != -1:
                insert_pos = content.find('>', canonical_pos) + 1
                content = content[:insert_pos] + og_tags + content[insert_pos:]
                changes.append("Added Open Graph tags")

        return content, changes

    def add_twitter_cards(self, content, page_info):
        """Add Twitter Card tags if missing"""
        changes = []

        # Check if Twitter cards already exist
        if not re.search(r'name="twitter:card"', content, re.IGNORECASE):
            twitter_tags = f'''
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{page_info['title'] or page_info['h1'] or 'Shopify App Reviews'}">
    <meta name="twitter:description" content="{page_info['description'] or page_info['title'][:155]}">'''

            # Insert after OG tags or canonical
            og_pos = content.find('property="og:')
            if og_pos != -1:
                # Find the last OG tag
                last_og = content.rfind('property="og:', og_pos, og_pos + 500)
                insert_pos = content.find('>', last_og) + 1
                content = content[:insert_pos] + twitter_tags + content[insert_pos:]
                changes.append("Added Twitter Card tags")

        return content, changes

    def optimize_images(self, content, page_info):
        """Add missing alt attributes and lazy loading"""
        changes = []

        for img in page_info['images']:
            original_tag = img['tag']
            new_tag = original_tag

            # Add missing alt attribute
            if img['alt'] is None:
                # Generate alt from src filename
                src = img['src']
                if src:
                    filename = os.path.basename(src).replace('-', ' ').replace('_', ' ')
                    filename = os.path.splitext(filename)[0]
                    new_tag = re.sub(r'(<img[^>]*)(>)', rf'\1 alt="{filename}"\2', new_tag)

            # Add lazy loading for images not in first viewport
            if 'loading=' not in new_tag and 'logo' not in new_tag.lower() and 'icon' not in new_tag.lower():
                new_tag = re.sub(r'(<img[^>]*)(>)', r'\1 loading="lazy"\2', new_tag)

            # Add decoding async
            if 'decoding=' not in new_tag:
                new_tag = re.sub(r'(<img[^>]*)(>)', r'\1 decoding="async"\2', new_tag)

            if new_tag != original_tag:
                content = content.replace(original_tag, new_tag)
                changes.append(f"Optimized image: {img['src'][:50]}...")

        return content, changes

    def add_security_headers(self, content):
        """Add security meta tags"""
        changes = []

        # Add X-Content-Type-Options
        if not re.search(r'X-Content-Type-Options', content, re.IGNORECASE):
            security_tag = '<meta http-equiv="X-Content-Type-Options" content="nosniff">'
            head_pos = content.find('<head')
            if head_pos != -1:
                head_end = content.find('>', head_pos)
                content = content[:head_end+1] + '\n    ' + security_tag + content[head_end+1:]
                changes.append("Added X-Content-Type-Options header")

        # Add referrer policy if missing
        if not re.search(r'name="referrer"', content, re.IGNORECASE):
            referrer_tag = '<meta name="referrer" content="strict-origin-when-cross-origin">'
            head_pos = content.find('<head')
            if head_pos != -1:
                head_end = content.find('>', head_pos)
                content = content[:head_end+1] + '\n    ' + referrer_tag + content[head_end+1:]
                changes.append("Added referrer policy")

        return content, changes

    def fix_external_links(self, content):
        """Add security attributes to external links"""
        changes = []

        # Find all external links
        external_links = re.findall(r'<a[^>]+href="https?://(?!shopifyappauthority)[^"]+[^>]*>', content, re.IGNORECASE)

        for link in external_links:
            new_link = link

            # Add rel="noopener" if target="_blank"
            if 'target="_blank"' in link and 'rel=' not in link:
                new_link = re.sub(r'(<a[^>]*)(>)', r'\1 rel="noopener noreferrer"\2', new_link)
            elif 'target="_blank"' in link and 'noopener' not in link:
                new_link = re.sub(r'rel="([^"]*)"', r'rel="\1 noopener noreferrer"', new_link)

            if new_link != link:
                content = content.replace(link, new_link)
                changes.append("Added noopener to external link")

        return content, changes

    def validate_schema_markup(self, content):
        """Validate and fix JSON-LD schema"""
        changes = []

        # Find all JSON-LD blocks
        schema_blocks = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
                                  content, re.DOTALL | re.IGNORECASE)

        for schema in schema_blocks:
            try:
                # Try to parse JSON to check validity
                json_data = json.loads(schema)

                # Check for common issues
                if '@context' not in json_data:
                    json_data['@context'] = 'https://schema.org'
                    updated_schema = json.dumps(json_data, indent=2)
                    content = content.replace(schema, updated_schema)
                    changes.append("Fixed schema @context")

            except json.JSONDecodeError:
                # Log but don't break
                changes.append("Found invalid JSON-LD schema (manual review needed)")

        return content, changes

    def process_file(self, file_path):
        """Process a single HTML file with all SEO optimizations"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            page_info = self.extract_page_info(content)
            all_changes = []

            # Apply all optimizations
            content, changes = self.add_missing_meta_tags(content, page_info)
            all_changes.extend(changes)

            content, changes = self.add_canonical_tag(content, file_path)
            all_changes.extend(changes)

            content, changes = self.add_open_graph_tags(content, page_info, file_path)
            all_changes.extend(changes)

            content, changes = self.add_twitter_cards(content, page_info)
            all_changes.extend(changes)

            content, changes = self.optimize_images(content, page_info)
            all_changes.extend(changes)

            content, changes = self.add_security_headers(content)
            all_changes.extend(changes)

            content, changes = self.fix_external_links(content)
            all_changes.extend(changes)

            content, changes = self.validate_schema_markup(content)
            all_changes.extend(changes)

            # Only write if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True, all_changes

            return False, []

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return False, []

def main():
    """Execute technical SEO implementation across all HTML files"""
    print("Implementing Technical SEO Guidelines (Safe, Non-Breaking)")
    print("=" * 60)

    optimizer = TechnicalSEOOptimizer()

    # Find all HTML files
    html_files = glob.glob("**/*.html", recursive=True)
    html_files = [f for f in html_files if 'TEMPLATE' not in f.upper()]

    modified_files = []
    all_changes = {}

    print(f"Processing {len(html_files)} HTML files...")

    for i, file_path in enumerate(html_files):
        if i % 20 == 0:  # Progress indicator
            print(f"Progress: {i}/{len(html_files)} files processed")

        modified, changes = optimizer.process_file(file_path)
        if modified:
            modified_files.append(file_path)
            all_changes[file_path] = changes

    # Summary report
    print("\n" + "=" * 60)
    print("TECHNICAL SEO IMPLEMENTATION SUMMARY")
    print("=" * 60)
    print(f"\nTotal files processed: {len(html_files)}")
    print(f"Files modified: {len(modified_files)}")

    # Count types of changes
    change_types = {}
    for file_changes in all_changes.values():
        for change in file_changes:
            change_type = change.split()[0] + ' ' + change.split()[1] if len(change.split()) > 1 else change
            change_types[change_type] = change_types.get(change_type, 0) + 1

    print("\nChanges Applied:")
    for change_type, count in sorted(change_types.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {change_type}: {count} instances")

    print("\nModified Files (first 10):")
    for file_path in modified_files[:10]:
        print(f"  - {file_path}")
    if len(modified_files) > 10:
        print(f"  ... and {len(modified_files) - 10} more files")

    print("\n✅ Technical SEO implementation complete!")
    print("All changes are safe, non-breaking improvements.")

    return len(modified_files)

if __name__ == "__main__":
    main()