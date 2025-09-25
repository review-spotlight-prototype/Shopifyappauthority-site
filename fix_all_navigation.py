#!/usr/bin/env python3
"""
Comprehensive script to add complete navigation menu to all pages and move affiliate disclosures to bottom.
"""

import os
import re
from pathlib import Path

# Complete navigation CSS styles
NAVIGATION_CSS = '''        /* Navigation Styles */
        .site-header {
            background: linear-gradient(180deg, #ffffff 0%, #fafafa 100%);
            border-bottom: 1px solid rgba(149, 191, 71, 0.2);
            position: sticky;
            top: 0;
            z-index: 1000;
            backdrop-filter: blur(10px);
        }

        .site-nav {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 70px;
        }

        .logo {
            font-size: 1.8rem;
            font-weight: bold;
            color: #95bf47;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            white-space: nowrap;
            line-height: 1;
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 50px;
            align-items: center;
        }

        .nav-links a {
            color: #4a5568;
            text-decoration: none;
            font-weight: 500;
            font-size: 1rem;
            transition: all 0.3s ease;
            padding: 0.8rem 1.2rem;
            border-radius: 10px;
            white-space: nowrap;
        }

        .nav-links a:hover, .nav-links a:focus {
            color: #95bf47;
            background: rgba(149, 191, 71, 0.08);
            transform: translateY(-1px);
            outline: none;
        }

        .dropdown {
            position: relative;
        }

        .dropdown-content {
            display: none;
            position: absolute;
            top: 100%;
            left: 0;
            background: white;
            min-width: 200px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            border-radius: 12px;
            padding: 12px 0;
            border: 1px solid rgba(149, 191, 71, 0.2);
            z-index: 1000;
        }

        .dropdown:hover .dropdown-content, .dropdown:focus-within .dropdown-content {
            display: block;
        }

        .dropdown-content a {
            display: block;
            padding: 0.7rem 1.2rem;
            color: #4a5568;
            text-decoration: none;
            transition: all 0.2s ease;
            border-radius: 0;
            font-size: 0.95rem;
        }

        .dropdown-content a:hover, .dropdown-content a:focus {
            background: linear-gradient(135deg, #95bf47 0%, #7fa83a 100%);
            color: white;
            transform: none;
            outline: none;
        }

        .mobile-menu-toggle {
            display: none;
            background: none;
            border: none;
            font-size: 1.5rem;
            color: #4a5568;
            cursor: pointer;
        }

        @media (max-width: 768px) {
            .site-nav {
                padding: 0 20px;
            }

            .nav-links {
                display: none;
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                background: white;
                flex-direction: column;
                gap: 0;
                padding: 0;
                box-shadow: 0 4px 20px rgba(0,0,0,0.15);
                z-index: 1000;
                max-height: 80vh;
                overflow-y: auto;
            }

            .nav-links.active {
                display: flex;
            }

            .nav-links > li {
                border-bottom: 1px solid #f1f5f9;
            }

            .nav-links > li > a {
                padding: 1rem 20px;
                border-radius: 0;
                display: block;
                font-weight: 500;
            }

            .mobile-menu-toggle {
                display: block;
            }

            .dropdown-content {
                position: static;
                display: none;
                box-shadow: none;
                border: none;
                background: #f8f9fa;
                padding: 0;
                margin: 0;
            }

            .dropdown.mobile-open .dropdown-content {
                display: block;
            }

            .dropdown-content a {
                padding: 0.75rem 40px;
                font-size: 0.9rem;
                color: #6b7280;
                border-bottom: 1px solid #e2e8f0;
            }

            .dropdown-content a:hover {
                background: #e2e8f0;
                color: #4a5568;
            }
        }'''

# Complete navigation HTML structure
NAVIGATION_HTML = '''    <header class="site-header">
        <nav class="site-nav">
            <a href="/" class="logo">🚀&nbsp;ShopifyAppAuthority</a>
            <ul class="nav-links">
                <li><a href="/best-shopify-apps-2025-ultimate-guide/">Best Tools</a></li>
                <li class="dropdown">
                    <a href="/app-categories/" aria-haspopup="true" aria-expanded="false">App Categories</a>
                    <div class="dropdown-content" role="menu">
                        <a href="/best-shopify-apps-email-marketing/" role="menuitem">Email Marketing</a>
                        <a href="/best-shopify-apps-conversion-optimization/" role="menuitem">Conversion & Sales</a>
                        <a href="/reviews-social-proof-apps/" role="menuitem">Reviews & Social Proof</a>
                        <a href="/best-shopify-apps-customer-service/" role="menuitem">Customer Service</a>
                        <a href="/best-shopify-apps-crm-sales/" role="menuitem">CRM & Sales Apps</a>
                        <a href="/best-shopify-apps-analytics-attribution/" role="menuitem">Analytics & Attribution</a>
                        <a href="/free-shopify-apps/" role="menuitem">Free Apps</a>
                    </div>
                </li>
                <li class="dropdown">
                    <a href="/faqs/" aria-haspopup="true" aria-expanded="false">Quick FAQs</a>
                    <div class="dropdown-content" role="menu">
                        <a href="/faqs/email-marketing-faq/" role="menuitem">Email Marketing FAQ</a>
                        <a href="/faqs/analytics-attribution-faq/" role="menuitem">Analytics & Attribution FAQ</a>
                        <a href="/faqs/crm-sales-faq/" role="menuitem">CRM & Sales FAQ</a>
                    </div>
                </li>
                <li class="dropdown">
                    <a href="/store-size/" aria-haspopup="true" aria-expanded="false">By Store Size</a>
                    <div class="dropdown-content" role="menu">
                        <a href="/apps-for-small-stores/" role="menuitem">Small Stores (0-1K orders/month)</a>
                        <a href="/apps-for-medium-stores/" role="menuitem">Medium Stores (1K-10K orders/month)</a>
                        <a href="/apps-for-enterprise/" role="menuitem">Enterprise (10K+ orders/month)</a>
                    </div>
                </li>
                <li><a href="/affiliate-disclosure/">Disclosure</a></li>
            </ul>
            <button class="mobile-menu-toggle" aria-label="Toggle mobile menu">☰</button>
        </nav>
    </header>

'''

# Mobile menu JavaScript
MOBILE_JS = '''
        // Mobile menu functionality
        document.addEventListener('DOMContentLoaded', function() {
            const mobileToggle = document.querySelector('.mobile-menu-toggle');
            const navLinks = document.querySelector('.nav-links');
            const dropdowns = document.querySelectorAll('.dropdown');

            // Mobile menu toggle
            if (mobileToggle && navLinks) {
                mobileToggle.addEventListener('click', function() {
                    navLinks.classList.toggle('active');
                });
            }

            // Mobile dropdown toggles
            dropdowns.forEach(dropdown => {
                const dropdownLink = dropdown.querySelector('a');
                if (dropdownLink) {
                    dropdownLink.addEventListener('click', function(e) {
                        if (window.innerWidth <= 768) {
                            e.preventDefault();

                            // Close other dropdowns
                            dropdowns.forEach(otherDropdown => {
                                if (otherDropdown !== dropdown) {
                                    otherDropdown.classList.remove('mobile-open');
                                }
                            });

                            // Toggle current dropdown
                            dropdown.classList.toggle('mobile-open');
                        }
                    });
                }
            });

            // Close mobile menu when clicking outside
            document.addEventListener('click', function(e) {
                if (!e.target.closest('.site-nav') && navLinks.classList.contains('active')) {
                    navLinks.classList.remove('active');
                }
            });

            // Close mobile menu on window resize
            window.addEventListener('resize', function() {
                if (window.innerWidth > 768) {
                    navLinks.classList.remove('active');
                    dropdowns.forEach(dropdown => {
                        dropdown.classList.remove('mobile-open');
                    });
                }
            });
        });'''

def has_complete_navigation(content):
    """Check if file has complete navigation structure."""
    required_elements = [
        '🚀.*ShopifyAppAuthority',
        'Best Tools',
        'App Categories',
        'Quick FAQs',
        'By Store Size',
        'Disclosure',
        'Email Marketing.*role="menuitem"',
        'Analytics & Attribution FAQ'
    ]

    for element in required_elements:
        if not re.search(element, content, re.IGNORECASE):
            return False
    return True

def add_navigation_to_file(file_path):
    """Add complete navigation to a single HTML file."""
    print(f"Processing {file_path}...")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already has complete navigation
        if has_complete_navigation(content):
            print(f"  [SKIP] {file_path} already has complete navigation")
            return False

        original_content = content

        # Step 1: Add navigation CSS
        if '</style>' in content:
            content = content.replace('</style>', f'{NAVIGATION_CSS}\n    </style>')
        else:
            # If no existing styles, add them before </head>
            head_match = re.search(r'</head>', content)
            if head_match:
                css_block = f'    <style>\n{NAVIGATION_CSS}\n    </style>\n'
                content = content.replace('</head>', f'{css_block}</head>')

        # Step 2: Add navigation HTML after <body>
        body_match = re.search(r'<body[^>]*>', content)
        if body_match:
            body_tag = body_match.group(0)
            content = content.replace(body_tag, f'{body_tag}\n{NAVIGATION_HTML}')

        # Step 3: Add mobile JavaScript
        if '</body>' in content:
            # Check if there's already a script tag
            if re.search(r'<script[^>]*>.*</script>', content, re.DOTALL):
                # Find the last script tag
                script_matches = list(re.finditer(r'(<script[^>]*>)(.*?)(</script>)', content, re.DOTALL))
                if script_matches:
                    last_script = script_matches[-1]
                    existing_js = last_script.group(2)
                    new_js = f'{existing_js}\n{MOBILE_JS}'
                    content = content.replace(last_script.group(0), f'{last_script.group(1)}{new_js}{last_script.group(3)}')
            else:
                # Add new script tag
                js_block = f'    <script>{MOBILE_JS}\n    </script>\n'
                content = content.replace('</body>', f'{js_block}</body>')

        # Step 4: Move affiliate disclosure to bottom if present in hero/top section
        content = move_affiliate_disclosure_to_bottom(content)

        # Only write if content actually changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  [UPDATED] {file_path}")
            return True
        else:
            print(f"  [NO CHANGE] {file_path}")
            return False

    except Exception as e:
        print(f"  [ERROR] {file_path}: {str(e)}")
        return False

def move_affiliate_disclosure_to_bottom(content):
    """Move affiliate disclosure from top/middle to bottom of page."""
    # Common affiliate disclosure patterns
    disclosure_patterns = [
        r'<div[^>]*style="[^"]*background:\s*#f8f9fa[^"]*"[^>]*>.*?<strong>Affiliate Disclosure:</strong>.*?</div>',
        r'<div[^>]*class="[^"]*affiliate[^"]*"[^>]*>.*?</div>',
        r'<div[^>]*>.*?<strong>Affiliate Disclosure:</strong>.*?</div>'
    ]

    disclosure_found = None

    # Find disclosure
    for pattern in disclosure_patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            disclosure_found = match.group(0)
            # Remove from current position
            content = content.replace(disclosure_found, '')
            break

    if disclosure_found:
        # Add before closing main or body tag
        if '</main>' in content:
            content = content.replace('</main>', f'    {disclosure_found}\n    </main>')
        elif '</body>' in content:
            content = content.replace('</body>', f'    {disclosure_found}\n</body>')

    return content

def main():
    """Main function to update all files."""
    base_dir = Path("C:/Projects/Shopifyappauthority-site")

    print("Starting comprehensive navigation and disclosure updates...")
    print(f"Base directory: {base_dir}")

    updated_count = 0
    skipped_count = 0
    failed_count = 0

    # Find all HTML files
    html_files = list(base_dir.glob('**/*.html'))

    # Filter out backup files and temporary files
    html_files = [f for f in html_files if not any(part.startswith('.') for part in f.parts)]

    print(f"Found {len(html_files)} HTML files to process")

    for file_path in html_files:
        result = add_navigation_to_file(file_path)
        if result is True:
            updated_count += 1
        elif result is False:
            skipped_count += 1
        else:
            failed_count += 1

    print(f"\nNavigation and disclosure update complete!")
    print(f"[UPDATED] {updated_count} files")
    print(f"[SKIPPED] {skipped_count} files")
    print(f"[FAILED] {failed_count} files")

    if failed_count == 0:
        print("All files processed successfully! 🎉")

if __name__ == "__main__":
    main()