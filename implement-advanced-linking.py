#!/usr/bin/env python3
"""
Internal Linking Implementation - Phase 3: Advanced Link Patterns
Following internal-linking-implementation.md guidelines for cross-category connections,
store size segmentation, and integration ecosystem links
"""

import os
import re
import glob

# Cross-category relationship mappings
CROSS_CATEGORY_LINKS = {
    'email marketing': {
        'related_categories': ['conversion optimization', 'analytics', 'crm'],
        'integration_mentions': ['klaviyo', 'mailchimp', 'hubspot'],
        'workflow_connections': ['sms marketing', 'social proof', 'analytics']
    },
    'conversion optimization': {
        'related_categories': ['email marketing', 'analytics', 'reviews'],
        'integration_mentions': ['optinmonster', 'unbounce', 'hotjar'],
        'workflow_connections': ['email capture', 'analytics tracking', 'social proof']
    },
    'crm': {
        'related_categories': ['email marketing', 'analytics', 'customer service'],
        'integration_mentions': ['hubspot', 'salesforce', 'klaviyo'],
        'workflow_connections': ['email automation', 'lead scoring', 'customer service']
    },
    'analytics': {
        'related_categories': ['email marketing', 'conversion optimization', 'crm'],
        'integration_mentions': ['google analytics', 'mixpanel', 'hotjar'],
        'workflow_connections': ['email tracking', 'conversion tracking', 'attribution']
    }
}

# Store size segmentation
STORE_SIZE_LINKS = {
    'small store': '/store-size/',
    'small stores': '/store-size/',
    'startup': '/store-size/',
    'new shopify store': '/store-size/',
    'beginning ecommerce': '/store-size/',
    '0-1k orders': '/store-size/',
    'under $10k': '/store-size/',
    'medium store': '/store-size/',
    'medium stores': '/store-size/',
    'growing business': '/store-size/',
    '1k-10k orders': '/store-size/',
    '$10k-$100k': '/store-size/',
    'enterprise': '/store-size/',
    'enterprise store': '/store-size/',
    'large business': '/store-size/',
    '10k+ orders': '/store-size/',
    'shopify plus': '/store-size/',
    '$100k+': '/store-size/'
}

# Integration ecosystem patterns
INTEGRATION_PATTERNS = {
    'klaviyo integration': '/klaviyo-review/',
    'mailchimp sync': '/mailchimp-review/',
    'hubspot crm': '/hubspot-review/',
    'google analytics': '/google-analytics-360-review/',
    'shopify plus': '/best-shopify-apps-2025-ultimate-guide/',
    'facebook pixel': '/best-shopify-apps-analytics-attribution/',
    'google ads': '/best-shopify-apps-analytics-attribution/',
    'abandoned cart': '/abandoned-cart-email-shopify/',
    'email automation': '/best-shopify-apps-email-marketing/',
    'sms marketing': '/postscript-review/',
    'live chat': '/livechat-review/',
    'customer reviews': '/reviews-social-proof-apps/'
}

def get_page_category(file_path):
    """Determine the category of the current page"""
    path_lower = file_path.lower()

    if 'email' in path_lower:
        return 'email marketing'
    elif any(term in path_lower for term in ['conversion', 'upsell', 'optinmonster', 'unbounce']):
        return 'conversion optimization'
    elif any(term in path_lower for term in ['crm', 'sales', 'hubspot', 'salesforce']):
        return 'crm'
    elif any(term in path_lower for term in ['analytics', 'attribution', 'mixpanel', 'hotjar']):
        return 'analytics'
    elif any(term in path_lower for term in ['review', 'social-proof', 'yotpo', 'judge']):
        return 'reviews'
    elif any(term in path_lower for term in ['customer-service', 'zendesk', 'gorgias']):
        return 'customer service'
    else:
        return 'general'

def add_cross_category_connections(content, current_category):
    """Add cross-category workflow connections"""
    if current_category not in CROSS_CATEGORY_LINKS:
        return content

    connections = CROSS_CATEGORY_LINKS[current_category]

    # Add workflow connection mentions
    workflow_patterns = {
        'email capture': (r'\b(email capture|lead capture|subscriber acquisition)\b',
                         '<a href="/best-shopify-apps-conversion-optimization/">email capture optimization</a>'),
        'analytics tracking': (r'\b(analytics tracking|conversion tracking|performance tracking)\b',
                              '<a href="/best-shopify-apps-analytics-attribution/">analytics tracking</a>'),
        'social proof': (r'\b(social proof|customer reviews|testimonials)\b',
                        '<a href="/reviews-social-proof-apps/">social proof apps</a>'),
        'crm integration': (r'\b(crm integration|customer management|lead scoring)\b',
                           '<a href="/best-shopify-apps-crm-sales/">CRM integration</a>'),
        'sms marketing': (r'\b(sms marketing|text messaging|mobile marketing)\b',
                         '<a href="/postscript-review/">SMS marketing</a>')
    }

    for connection, (pattern, replacement) in workflow_patterns.items():
        # Only add if not already linked and context is appropriate
        if connection in connections.get('workflow_connections', []):
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches and f'href=' not in re.search(pattern, content, re.IGNORECASE).group():
                content = re.sub(pattern, replacement, content, count=1, flags=re.IGNORECASE)

    return content

def add_store_size_segmentation(content):
    """Add store size segmentation links when size mentions occur"""
    for size_term, size_url in STORE_SIZE_LINKS.items():
        pattern = rf'\b({re.escape(size_term)})\b'

        # Check if term exists and isn't already linked
        if re.search(pattern, content, re.IGNORECASE) and size_url not in content:
            # Create contextual link
            contextual_replacement = f'<a href="{size_url}">{size_term}</a>'
            content = re.sub(pattern, contextual_replacement, content, count=1, flags=re.IGNORECASE)

    return content

def add_integration_ecosystem_links(content):
    """Add integration ecosystem links for mentioned platforms"""
    for integration_term, integration_url in INTEGRATION_PATTERNS.items():
        pattern = rf'\b({re.escape(integration_term)})\b'

        # Check if integration is mentioned but not already linked to that specific page
        if re.search(pattern, content, re.IGNORECASE) and integration_url not in content:
            # Create contextual integration link
            replacement = f'<a href="{integration_url}">{integration_term}</a>'
            content = re.sub(pattern, replacement, content, count=1, flags=re.IGNORECASE)

    return content

def add_hub_page_connections(content, file_path):
    """Connect to hub pages from pillar content"""
    if 'best-shopify-apps-2025' in file_path or 'index.html' == os.path.basename(file_path):
        # Add strategic links to major category pages within content
        category_mentions = {
            'email marketing apps': '/best-shopify-apps-email-marketing/',
            'conversion optimization tools': '/best-shopify-apps-conversion-optimization/',
            'crm and sales apps': '/best-shopify-apps-crm-sales/',
            'analytics and attribution': '/best-shopify-apps-analytics-attribution/',
            'review and social proof': '/reviews-social-proof-apps/',
            'customer service tools': '/best-shopify-apps-customer-service/'
        }

        for mention, category_url in category_mentions.items():
            pattern = rf'\b({re.escape(mention)})\b'
            if re.search(pattern, content, re.IGNORECASE) and category_url not in content:
                replacement = f'<a href="{category_url}">{mention}</a>'
                content = re.sub(pattern, replacement, content, count=1, flags=re.IGNORECASE)

    return content

def enhance_related_sections(content):
    """Enhance existing related sections with better categorization"""
    if 'related-apps' not in content:
        return content

    # Find and enhance the related section
    related_section_pattern = r'(<section class="related-apps".*?</section>)'
    match = re.search(related_section_pattern, content, re.DOTALL)

    if match:
        current_section = match.group(1)

        # Add category context to related links
        enhanced_section = current_section.replace(
            'Related App Reviews',
            'Related App Reviews & Categories'
        )

        # Add category links within related section
        if 'Email Marketing' not in enhanced_section:
            category_links = '''
                <li style="margin-bottom: 0.5rem;">
                    <a href="/best-shopify-apps-email-marketing/" style="color: #4A90E2; text-decoration: none; font-weight: 500;">
                        Browse All Email Marketing Apps →
                    </a>
                </li>'''

            enhanced_section = enhanced_section.replace('</ul>', category_links + '\n            </ul>')

        content = content.replace(current_section, enhanced_section)

    return content

def process_file_advanced(file_path):
    """Process a single HTML file for advanced linking patterns"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        current_category = get_page_category(file_path)

        # Apply advanced linking rules
        content = add_cross_category_connections(content, current_category)
        content = add_store_size_segmentation(content)
        content = add_integration_ecosystem_links(content)
        content = add_hub_page_connections(content, file_path)
        content = enhance_related_sections(content)

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
    """Implement Phase 3: Advanced Link Patterns"""
    print("Implementing Phase 3: Advanced Link Patterns")

    # Find all HTML files
    html_files = glob.glob("**/*.html", recursive=True)

    modified_files = []

    for file_path in html_files:
        # Skip template files
        if 'TEMPLATE' in file_path.upper():
            continue

        print(f"Processing: {file_path}")
        if process_file_advanced(file_path):
            modified_files.append(file_path)

    print(f"\nPhase 3 Advanced Link Patterns Complete!")
    print(f"Files processed: {len(html_files)}")
    print(f"Files modified: {len(modified_files)}")

    if modified_files:
        print("\nModified files:")
        for file_path in modified_files[:10]:  # Show first 10
            print(f"  - {file_path}")
        if len(modified_files) > 10:
            print(f"  ... and {len(modified_files) - 10} more files")

    # Quality check summary
    print(f"\nAdvanced patterns applied:")
    print(f"- Cross-category workflow connections (email ↔ CRO, CRM ↔ analytics)")
    print(f"- Store size segmentation links (small/medium/enterprise)")
    print(f"- Integration ecosystem connections (Klaviyo, Shopify Plus, etc.)")
    print(f"- Enhanced hub page connections from pillar content")
    print(f"- Improved related content sections with category context")

    return len(modified_files)

if __name__ == "__main__":
    main()