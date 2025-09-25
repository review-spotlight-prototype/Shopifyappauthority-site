#!/usr/bin/env python3
"""
Fix duplicate mobile navigation scripts across all HTML files
"""

import os
import re
import glob

def fix_mobile_navigation_in_file(file_path):
    """Fix duplicate mobile navigation scripts in a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Remove all existing mobile navigation script blocks
        patterns_to_remove = [
            r'// Mobile navigation functionality.*?(?=// [A-Z]|\s*</script>|\s*window\.addEventListener)',
            r'// Mobile menu functionality.*?(?=// [A-Z]|\s*</script>|\s*window\.addEventListener)',
            r'document\.addEventListener\([\'"]DOMContentLoaded[\'"], function\(\) \{[\s\S]*?const mobileToggle = document\.querySelector\([\'"]\.mobile-menu-toggle[\'"],\);[\s\S]*?\}\);',
        ]

        for pattern in patterns_to_remove:
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)

        # Clean up any remaining duplicate mobile navigation code
        # Remove duplicate event listeners for mobile toggle
        content = re.sub(
            r'(document\.addEventListener\([\'"]DOMContentLoaded[\'"], function\(\) \{[\s\S]*?)(?=document\.addEventListener\([\'"]DOMContentLoaded[\'"], function\(\) \{[\s\S]*?mobileToggle)',
            r'\1',
            content,
            flags=re.DOTALL
        )

        # Insert clean, working mobile navigation script before the closing </script> tag
        mobile_nav_script = '''        // Mobile navigation functionality
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
        });'''

        # Find the last script tag and insert before closing
        script_insertion_point = content.rfind('</script>')
        if script_insertion_point != -1:
            # Remove any existing mobile nav code right before this point
            before_script = content[:script_insertion_point]
            after_script = content[script_insertion_point:]

            # Clean up any remaining mobile nav fragments
            before_script = re.sub(r'// Mobile.*?(?=\s*</script>)', '', before_script, flags=re.DOTALL)
            before_script = re.sub(r'\s*window\.addEventListener\([\'"]DOMContentLoaded[\'"], checkCookieConsent\);?\s*$', '', before_script.strip())

            # Insert the clean mobile navigation script
            content = before_script + '\n' + mobile_nav_script + '\n    ' + after_script

        # Clean up extra whitespace
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

        # Only write if content changed significantly
        if content != original_content and len(content) > 100:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix mobile navigation across all HTML files"""
    print("Fixing mobile navigation functionality...")

    # Find all HTML files
    html_files = glob.glob("**/*.html", recursive=True)

    modified_files = []

    for file_path in html_files:
        # Skip template files
        if 'TEMPLATE' in file_path.upper():
            continue

        print(f"Processing: {file_path}")
        if fix_mobile_navigation_in_file(file_path):
            modified_files.append(file_path)

    print(f"\nMobile navigation fix complete!")
    print(f"Files processed: {len(html_files)}")
    print(f"Files modified: {len(modified_files)}")

    if modified_files:
        print("\nModified files:")
        for file_path in modified_files[:10]:  # Show first 10
            print(f"  - {file_path}")
        if len(modified_files) > 10:
            print(f"  ... and {len(modified_files) - 10} more files")

    return len(modified_files)

if __name__ == "__main__":
    main()