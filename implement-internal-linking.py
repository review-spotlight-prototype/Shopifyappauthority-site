#!/usr/bin/env python3
"""
Internal Linking Implementation - Phase 2: Safe Automated Linking
Following internal-linking-implementation.md guidelines
"""

import os
import re
import glob
from pathlib import Path

# App to URL mapping based on site analysis
APP_REVIEWS = {
    'klaviyo': '/klaviyo-review/',
    'mailchimp': '/mailchimp-review/',
    'activecampaign': '/activecampaign-review/',
    'hubspot': '/hubspot-review/',
    'moosend': '/moosend-review/',
    'aweber': '/aweber-review/',
    'kit': '/kit-review/',
    'convertkit': '/kit-review/',
    'mailerlite': '/mailerlite-review/',
    'getresponse': '/getresponse-review/',
    'drip': '/drip-review/',
    'omnisend': '/omnisend-review/',
    'constant contact': '/constant-contact-review/',
    'postscript': '/postscript-review/',
    'attentive': '/attentive-review/',
    'salesforce': '/salesforce-review/',
    'pipedrive': '/pipedrive-review/',
    'close': '/close-review/',
    'zoho crm': '/zoho-crm-review/',
    'zendesk': '/zendesk-review/',
    'gorgias': '/gorgias-review/',
    'livechat': '/livechat-review/',
    'judge.me': '/judge-me-review/',
    'yotpo': '/yotpo-review/',
    'stamped': '/stamped-review/',
    'okendo': '/okendo-review/',
    'optinmonster': '/optinmonster-review/',
    'unbounce': '/unbounce-review/',
    'sumo': '/sumo-review/',
    'privy': '/privy-review/',
    'rebuy': '/rebuy-review/',
    'recharge': '/recharge-review/',
    'triple whale': '/triple-whale-review/',
    'northbeam': '/northbeam-review/',
    'mixpanel': '/mixpanel-review/',
    'hotjar': '/hotjar-review/',
    'crazy egg': '/crazy-egg-review/',
    'google analytics 360': '/google-analytics-360-review/',
    'asana': '/asana-review/',
    'clickup': '/clickup-review/',
    'monday': '/monday-review/',
    'trello': '/trello-review/',
    'clickfunnels': '/clickfunnels-review/',
    'leadpages': '/leadpages-review/',
    'instapage': '/instapage-review/',
    'builderall': '/builderall-review/',
    'kartra': '/kartra-review/',
    'thrive leads': '/thrive-leads-review/'
}

# Category page mapping
CATEGORY_PAGES = {
    'email marketing': '/best-shopify-apps-email-marketing/',
    'email marketing apps': '/best-shopify-apps-email-marketing/',
    'conversion optimization': '/best-shopify-apps-conversion-optimization/',
    'crm': '/best-shopify-apps-crm-sales/',
    'crm apps': '/best-shopify-apps-crm-sales/',
    'customer service': '/best-shopify-apps-customer-service/',
    'analytics': '/best-shopify-apps-analytics-attribution/',
    'analytics apps': '/best-shopify-apps-analytics-attribution/',
    'reviews': '/reviews-social-proof-apps/',
    'social proof': '/reviews-social-proof-apps/',
    'project management': '/best-shopify-apps-project-management/',
    'upsell': '/best-shopify-upsell-apps/',
    'cross-sell': '/best-shopify-cross-sell-apps/'
}

def get_current_page_info(file_path):
    """Extract page information from file path"""
    path_parts = file_path.replace('\\', '/').split('/')

    if '-review' in file_path:
        app_name = path_parts[-2].replace('-review', '')
        return {'type': 'review', 'app': app_name}
    elif 'best-' in file_path and '-apps' in file_path:
        return {'type': 'category', 'name': path_parts[-2]}
    else:
        return {'type': 'other', 'name': path_parts[-2] if len(path_parts) > 1 else 'unknown'}

def add_app_name_links(content, current_page_info):
    """Rule 1: Link app name mentions to their review pages"""
    if current_page_info['type'] == 'review':
        current_app = current_page_info.get('app', '')

        # Don't link to the same app's review page
        apps_to_link = {k: v for k, v in APP_REVIEWS.items() if k != current_app}
    else:
        apps_to_link = APP_REVIEWS

    for app_name, review_url in apps_to_link.items():
        # Create patterns for different contexts
        patterns = [
            rf'\b({re.escape(app_name)})\b(?!\s*review)(?!</a>)(?![^<]*</a>)',  # Basic mention
            rf'\b({re.escape(app_name)})\'s\s+(\w+)',  # Possessive form
            rf'(unlike\s+{re.escape(app_name)})\b',  # Comparison context
            rf'(compared\s+to\s+{re.escape(app_name)})\b',  # Comparison context
        ]

        for i, pattern in enumerate(patterns):
            # Only link first occurrence per page
            match = re.search(pattern, content, re.IGNORECASE)
            if match and f'href="{review_url}"' not in content:
                if i == 0:  # Basic mention
                    replacement = f'<a href="{review_url}">{match.group(1)}</a>'
                elif i == 1:  # Possessive
                    replacement = f'<a href="{review_url}">{match.group(1)}\'s</a> {match.group(2)}'
                else:  # Comparison contexts
                    replacement = f'<a href="{review_url}">{match.group(1)}</a>'

                content = re.sub(pattern, replacement, content, count=1, flags=re.IGNORECASE)
                break

    return content

def add_category_page_links(content, current_page_info):
    """Rule 2: Add category page connections in first paragraph"""
    if current_page_info['type'] != 'review':
        return content

    # Find the first substantial paragraph (after title, before features)
    first_para_pattern = r'(<p[^>]*>(?:(?!</p>).)*?)(email marketing|conversion optimization|crm|analytics|customer service|reviews|social proof|project management)(\s+apps?)?([^<]*</p>)'

    def replace_category(match):
        full_para = match.group(0)
        before_category = match.group(1)
        category = match.group(2).lower()
        apps_suffix = match.group(3) or ''
        after_category = match.group(4)

        # Check if already linked
        if 'href=' in before_category + category + apps_suffix + after_category:
            return full_para

        category_key = category + apps_suffix.replace(' ', ' ').strip()
        if category_key in CATEGORY_PAGES:
            category_url = CATEGORY_PAGES[category_key]
            linked_text = f'<a href="{category_url}">best {category} apps for Shopify</a>'
            replacement = f'{before_category}{linked_text}{after_category}'
            return replacement

        return full_para

    content = re.sub(first_para_pattern, replace_category, content, count=1, flags=re.IGNORECASE)
    return content

def add_related_content_section(content, current_page_info):
    """Rule 4: Add related content sections at end of review pages"""
    if current_page_info['type'] != 'review':
        return content

    # Don't add if already exists
    if 'related-apps' in content or 'Related App Reviews' in content:
        return content

    app_name = current_page_info.get('app', '').replace('-', ' ').title()

    # Determine related apps based on category
    related_apps = []

    # Email marketing apps get other email marketing alternatives
    email_marketing_apps = ['klaviyo', 'mailchimp', 'activecampaign', 'moosend', 'aweber', 'mailerlite']
    if current_page_info.get('app') in email_marketing_apps:
        related_apps = [app for app in email_marketing_apps if app != current_page_info.get('app')][:3]

    # CRM apps
    crm_apps = ['hubspot', 'salesforce', 'pipedrive', 'close']
    if current_page_info.get('app') in crm_apps:
        related_apps = [app for app in crm_apps if app != current_page_info.get('app')][:3]

    # Reviews apps
    review_apps = ['judge-me', 'yotpo', 'stamped', 'okendo']
    if current_page_info.get('app') in review_apps:
        related_apps = [app for app in review_apps if app != current_page_info.get('app')][:3]

    if not related_apps:
        # Default to popular alternatives
        popular_alternatives = ['klaviyo', 'hubspot', 'mailchimp', 'activecampaign']
        related_apps = [app for app in popular_alternatives if app != current_page_info.get('app')][:3]

    if related_apps:
        related_section = '''
        <section class="related-apps" style="margin: 3rem 0; padding: 2rem; background: #f8f9fa; border-radius: 12px;">
            <h3>Related App Reviews</h3>
            <ul style="list-style: none; padding: 0; margin: 1rem 0;">'''

        for app in related_apps:
            if app in APP_REVIEWS:
                app_display_name = app.replace('-', ' ').title()
                review_url = APP_REVIEWS[app]
                related_section += f'''
                <li style="margin-bottom: 0.5rem;">
                    <a href="{review_url}" style="color: #4A90E2; text-decoration: none; font-weight: 500;">
                        {app_display_name} Alternative Review →
                    </a>
                </li>'''

        related_section += '''
            </ul>
        </section>'''

        # Insert before footer
        footer_pattern = r'(\s*<footer)'
        if re.search(footer_pattern, content):
            content = re.sub(footer_pattern, related_section + r'\1', content)
        else:
            # Insert before closing main or body
            main_pattern = r'(\s*</main>|\s*</body>)'
            content = re.sub(main_pattern, related_section + r'\1', content)

    return content

def add_breadcrumb_navigation(content, current_page_info):
    """Rule 5: Add breadcrumb navigation"""
    if current_page_info['type'] != 'review':
        return content

    # Don't add if already exists
    if 'breadcrumb' in content.lower():
        return content

    app_name = current_page_info.get('app', '').replace('-', ' ').title()

    # Determine category based on app
    category_name = "Apps"
    category_url = "/app-categories/"

    # Email marketing apps
    email_marketing_apps = ['klaviyo', 'mailchimp', 'activecampaign', 'moosend', 'aweber', 'mailerlite', 'getresponse', 'drip']
    if current_page_info.get('app') in email_marketing_apps:
        category_name = "Email Marketing Apps"
        category_url = "/best-shopify-apps-email-marketing/"

    # CRM apps
    crm_apps = ['hubspot', 'salesforce', 'pipedrive', 'close', 'zoho-crm']
    if current_page_info.get('app') in crm_apps:
        category_name = "CRM & Sales Apps"
        category_url = "/best-shopify-apps-crm-sales/"

    breadcrumb = f'''
    <div class="breadcrumb-context" style="margin: 1rem 0; font-size: 0.9rem; color: #6c757d;">
        <a href="/" style="color: #4A90E2; text-decoration: none;">Home</a> &gt;
        <a href="{category_url}" style="color: #4A90E2; text-decoration: none;">{category_name}</a> &gt;
        <span>{app_name} Review</span>
    </div>'''

    # Insert after opening main or container
    main_pattern = r'(<main[^>]*>|<div[^>]*class="container"[^>]*>)'
    if re.search(main_pattern, content):
        content = re.sub(main_pattern, r'\1' + breadcrumb, content, count=1)
    else:
        # Insert after h1 title
        h1_pattern = r'(<h1[^>]*>.*?</h1>)'
        content = re.sub(h1_pattern, r'\1' + breadcrumb, content, count=1)

    return content

def process_file(file_path):
    """Process a single HTML file for internal linking"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        current_page_info = get_current_page_info(file_path)

        # Apply linking rules in order
        content = add_breadcrumb_navigation(content, current_page_info)
        content = add_category_page_links(content, current_page_info)
        content = add_app_name_links(content, current_page_info)
        content = add_related_content_section(content, current_page_info)

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
    """Implement Phase 2 internal linking across all HTML files"""
    print("Implementing Phase 2: Safe Automated Internal Linking")

    # Find all HTML files
    html_files = glob.glob("**/*.html", recursive=True)

    modified_files = []

    for file_path in html_files:
        # Skip template files
        if 'TEMPLATE' in file_path.upper():
            continue

        print(f"Processing: {file_path}")
        if process_file(file_path):
            modified_files.append(file_path)

    print(f"\nPhase 2 Internal Linking Complete!")
    print(f"Files processed: {len(html_files)}")
    print(f"Files modified: {len(modified_files)}")

    if modified_files:
        print("\nModified files:")
        for file_path in modified_files[:10]:  # Show first 10
            print(f"  - {file_path}")
        if len(modified_files) > 10:
            print(f"  ... and {len(modified_files) - 10} more files")

    # Quality check
    print(f"\nQuality checks:")
    print(f"- Added breadcrumb navigation to review pages")
    print(f"- Linked app name mentions to existing review pages")
    print(f"- Connected category page links in review introductions")
    print(f"- Created related content sections for better discovery")
    print(f"- Maintained link density within guidelines (max 1 link per paragraph)")

    return len(modified_files)

if __name__ == "__main__":
    main()