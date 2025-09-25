#!/usr/bin/env python3
"""
Quality Assurance Validation for Internal Linking Implementation
Following internal-linking-implementation.md quality checklist
"""

import os
import re
import glob
from urllib.parse import urljoin, urlparse
from collections import defaultdict, Counter

def extract_internal_links(content, file_path):
    """Extract all internal links from HTML content"""
    links = []

    # Find all href attributes
    link_pattern = r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>'
    matches = re.findall(link_pattern, content, re.DOTALL | re.IGNORECASE)

    for href, anchor_text in matches:
        # Skip external links, mailto, tel, etc.
        if href.startswith(('http://', 'https://', 'mailto:', 'tel:', '#')):
            continue

        # Clean anchor text
        anchor_text = re.sub(r'<[^>]+>', '', anchor_text).strip()

        links.append({
            'url': href,
            'anchor_text': anchor_text,
            'source_file': file_path
        })

    return links

def check_link_exists(url):
    """Check if target file exists for internal link"""
    # Convert URL to file path
    if url.startswith('/'):
        url = url[1:]  # Remove leading slash

    # Handle index.html default
    if url.endswith('/'):
        url += 'index.html'
    elif not url.endswith('.html'):
        url += '/index.html'

    file_path = url.replace('/', os.sep)
    return os.path.exists(file_path)

def analyze_anchor_text_quality(anchor_text):
    """Analyze anchor text for quality and variety"""
    quality_score = 0
    issues = []

    # Length check
    if len(anchor_text) < 3:
        issues.append("Too short")
    elif len(anchor_text) > 100:
        issues.append("Too long")
    else:
        quality_score += 1

    # Generic text check
    generic_terms = ['click here', 'read more', 'here', 'this', 'link']
    if any(term in anchor_text.lower() for term in generic_terms):
        issues.append("Generic anchor text")
    else:
        quality_score += 1

    # Descriptive content check
    if any(keyword in anchor_text.lower() for keyword in ['review', 'app', 'best', 'shopify', 'marketing']):
        quality_score += 1
    else:
        issues.append("Lacks descriptive keywords")

    return quality_score, issues

def check_link_density(content):
    """Check link density per content section"""
    # Remove script, style, and other non-content tags
    content_only = re.sub(r'<(script|style|nav|header|footer)[^>]*>.*?</\1>', '', content, flags=re.DOTALL | re.IGNORECASE)

    # Count words
    text_content = re.sub(r'<[^>]+>', '', content_only)
    words = len(text_content.split())

    # Count internal links
    internal_links = len(re.findall(r'<a[^>]+href=["\'][^"\']*["\'][^>]*>', content_only))

    if words > 0:
        link_density = (internal_links / words) * 1000  # Links per 1000 words
        return link_density, internal_links, words
    else:
        return 0, internal_links, words

def validate_content_flow(content):
    """Check that links don't disrupt content flow"""
    issues = []

    # Check for links in headings (should be minimal)
    heading_links = re.findall(r'<h[1-6][^>]*>.*?<a[^>]*>.*?</a>.*?</h[1-6]>', content, re.DOTALL)
    if len(heading_links) > 2:
        issues.append(f"Too many links in headings ({len(heading_links)})")

    # Check for paragraph with too many links
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
    for i, para in enumerate(paragraphs):
        para_links = len(re.findall(r'<a[^>]+href=', para))
        if para_links > 2:
            issues.append(f"Paragraph {i+1} has {para_links} links (max recommended: 1)")

    # Check for consecutive links (might be spammy)
    consecutive_links = re.findall(r'</a>\s*<a[^>]+href=', content)
    if len(consecutive_links) > 3:
        issues.append(f"Too many consecutive links ({len(consecutive_links)})")

    return issues

def analyze_single_file(file_path):
    """Analyze a single HTML file for link quality"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        results = {
            'file': file_path,
            'links': extract_internal_links(content, file_path),
            'link_density': check_link_density(content),
            'content_flow_issues': validate_content_flow(content),
            'broken_links': [],
            'anchor_text_issues': []
        }

        # Check for broken links
        for link in results['links']:
            if not check_link_exists(link['url']):
                results['broken_links'].append(link)

        # Analyze anchor text quality
        for link in results['links']:
            quality_score, issues = analyze_anchor_text_quality(link['anchor_text'])
            if issues:
                results['anchor_text_issues'].append({
                    'url': link['url'],
                    'anchor_text': link['anchor_text'],
                    'issues': issues,
                    'quality_score': quality_score
                })

        return results

    except Exception as e:
        return {'file': file_path, 'error': str(e)}

def generate_quality_report(all_results):
    """Generate comprehensive quality assurance report"""
    total_files = len(all_results)
    total_links = sum(len(r.get('links', [])) for r in all_results)
    broken_links = sum(len(r.get('broken_links', [])) for r in all_results)
    files_with_issues = sum(1 for r in all_results if r.get('content_flow_issues', []) or r.get('anchor_text_issues', []))

    print("\n" + "="*60)
    print("INTERNAL LINKING QUALITY ASSURANCE REPORT")
    print("="*60)

    print(f"\n📊 OVERVIEW:")
    print(f"   Files analyzed: {total_files}")
    print(f"   Total internal links: {total_links}")
    print(f"   Broken links: {broken_links}")
    print(f"   Files with quality issues: {files_with_issues}")

    # Link density analysis
    print(f"\n🔗 LINK DENSITY ANALYSIS:")
    high_density_files = 0
    low_density_files = 0

    for result in all_results:
        if 'link_density' in result:
            density, links, words = result['link_density']
            if density > 8:  # More than 8 links per 1000 words
                high_density_files += 1
            elif density < 2:  # Less than 2 links per 1000 words
                low_density_files += 1

    print(f"   High density files (>8 links/1000 words): {high_density_files}")
    print(f"   Low density files (<2 links/1000 words): {low_density_files}")
    print(f"   Optimal density files: {total_files - high_density_files - low_density_files}")

    # Anchor text analysis
    print(f"\n📝 ANCHOR TEXT QUALITY:")
    anchor_text_counter = Counter()
    generic_anchors = 0

    for result in all_results:
        for link in result.get('links', []):
            anchor_text_counter[link['anchor_text'].lower()] += 1
            if any(generic in link['anchor_text'].lower() for generic in ['click here', 'read more', 'here']):
                generic_anchors += 1

    repeated_anchors = sum(1 for count in anchor_text_counter.values() if count > 5)
    print(f"   Unique anchor texts: {len(anchor_text_counter)}")
    print(f"   Over-repeated anchors (>5 uses): {repeated_anchors}")
    print(f"   Generic anchor texts: {generic_anchors}")

    # Most common broken links
    if broken_links > 0:
        print(f"\n❌ BROKEN LINKS ({broken_links} total):")
        broken_urls = Counter()
        for result in all_results:
            for link in result.get('broken_links', []):
                broken_urls[link['url']] += 1

        for url, count in broken_urls.most_common(10):
            print(f"   {url} (appears in {count} files)")

    # Content flow issues
    print(f"\n📋 CONTENT FLOW ANALYSIS:")
    total_flow_issues = sum(len(r.get('content_flow_issues', [])) for r in all_results)
    print(f"   Files with content flow issues: {files_with_issues}")
    print(f"   Total content flow issues: {total_flow_issues}")

    # Quality score
    quality_percentage = max(0, 100 - (broken_links / max(total_links, 1) * 100) - (files_with_issues / total_files * 20))
    print(f"\n🎯 OVERALL QUALITY SCORE: {quality_percentage:.1f}/100")

    if quality_percentage >= 90:
        print("   Status: EXCELLENT - Ready for deployment")
    elif quality_percentage >= 75:
        print("   Status: GOOD - Minor improvements recommended")
    elif quality_percentage >= 60:
        print("   Status: FAIR - Some issues need attention")
    else:
        print("   Status: NEEDS WORK - Significant issues require fixing")

    return quality_percentage

def main():
    """Run comprehensive quality assurance validation"""
    print("Running Internal Linking Quality Assurance...")

    # Find all HTML files
    html_files = glob.glob("**/*.html", recursive=True)
    html_files = [f for f in html_files if 'TEMPLATE' not in f.upper()]

    all_results = []

    print(f"\nAnalyzing {len(html_files)} files...")

    for i, file_path in enumerate(html_files):
        if i % 20 == 0:  # Progress indicator
            print(f"Progress: {i}/{len(html_files)} files analyzed")

        result = analyze_single_file(file_path)
        all_results.append(result)

    # Generate comprehensive report
    quality_score = generate_quality_report(all_results)

    # Save detailed results for debugging
    print(f"\nValidation complete!")

    if quality_score >= 75:
        print("✅ Internal linking implementation passes quality assurance")
        return True
    else:
        print("⚠️  Internal linking implementation needs improvements before deployment")
        return False

if __name__ == "__main__":
    success = main()