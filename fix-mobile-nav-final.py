#!/usr/bin/env python3
"""
Final fix for mobile navigation - ensure proper script placement
"""

import os
import re
import glob

def fix_mobile_nav_final(file_path):
    """Fix mobile navigation script placement"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Remove any mobile navigation code that got placed in wrong script tags
        content = re.sub(r'(<script src="/assets/cookie-consent\.js">[^<]*?)// Mobile navigation functionality.*?(?=</script>)', r'\1', content, flags=re.DOTALL)

        # Ensure clean mobile navigation script exists before closing body tag
        mobile_nav_script = '''    <script>
        // Mobile navigation functionality
        document.addEventListener('DOMContentLoaded', function() {
            const mobileToggle = document.querySelector('.mobile-menu-toggle');
            const navLinks = document.querySelector('.nav-links');
            const dropdowns = document.querySelectorAll('.dropdown');

            // Mobile menu toggle button
            if (mobileToggle && navLinks) {
                mobileToggle.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    navLinks.classList.toggle('active');
                    this.textContent = navLinks.classList.contains('active') ? '✕' : '☰';
                });
            }

            // Mobile dropdown toggles
            dropdowns.forEach(dropdown => {
                const dropdownLink = dropdown.querySelector('a');
                if (dropdownLink) {
                    dropdownLink.addEventListener('click', function(e) {
                        if (window.innerWidth <= 768) {
                            e.preventDefault();
                            dropdowns.forEach(otherDropdown => {
                                if (otherDropdown !== dropdown) {
                                    otherDropdown.classList.remove('mobile-open');
                                }
                            });
                            dropdown.classList.toggle('mobile-open');
                        }
                    });
                }
            });

            // Close mobile menu when clicking outside
            document.addEventListener('click', function(e) {
                if (window.innerWidth <= 768 && navLinks) {
                    if (!e.target.closest('nav') && !e.target.closest('.mobile-menu-toggle')) {
                        navLinks.classList.remove('active');
                        if (mobileToggle) {
                            mobileToggle.textContent = '☰';
                        }
                        dropdowns.forEach(dropdown => {
                            dropdown.classList.remove('mobile-open');
                        });
                    }
                }
            });

            // Close mobile menu on window resize
            window.addEventListener('resize', function() {
                if (window.innerWidth > 768 && navLinks) {
                    navLinks.classList.remove('active');
                    if (mobileToggle) {
                        mobileToggle.textContent = '☰';
                    }
                    dropdowns.forEach(dropdown => {
                        dropdown.classList.remove('mobile-open');
                    });
                }
            });
        });
    </script>'''

        # Fix cookie consent script tag
        content = re.sub(r'<script src="/assets/cookie-consent\.js">[^<]*</script>', '<script src="/assets/cookie-consent.js"></script>', content)

        # Add mobile nav script before closing body tag if not already there
        if 'Mobile navigation functionality' not in content:
            content = content.replace('</body>', mobile_nav_script + '\n</body>')

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
    """Final fix for mobile navigation"""
    print("Applying final mobile navigation fix...")

    html_files = glob.glob("**/*.html", recursive=True)
    modified_files = []

    for file_path in html_files:
        if 'TEMPLATE' in file_path.upper():
            continue

        print(f"Processing: {file_path}")
        if fix_mobile_nav_final(file_path):
            modified_files.append(file_path)

    print(f"\nFinal mobile navigation fix complete!")
    print(f"Files processed: {len(html_files)}")
    print(f"Files modified: {len(modified_files)}")

    return len(modified_files)

if __name__ == "__main__":
    main()