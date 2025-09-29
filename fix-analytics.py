import os
import re

def fix_analytics():
    """Fix Google Analytics implementation across all HTML files"""

    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk('.'):
        if 'node_modules' in root or '.git' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))

    fixed_files = []
    issues_found = {}

    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            issues = []

            # 1. Fix duplicate or incorrect GA IDs
            if 'GA_MEASUREMENT_ID' in content:
                content = content.replace('GA_MEASUREMENT_ID', 'G-J09TH92K0M')
                issues.append('Fixed placeholder GA ID')

            # 2. Remove inline onclick gtag events (we'll handle via event delegation)
            onclick_pattern = r'onclick="gtag\([^"]*\)"'
            if re.search(onclick_pattern, content):
                content = re.sub(onclick_pattern, '', content)
                issues.append('Removed inline onclick tracking')

            # 3. Ensure only one GA script tag
            ga_script_pattern = r'<script async src="https://www\.googletagmanager\.com/gtag/js\?id=[^"]+"></script>'
            ga_scripts = re.findall(ga_script_pattern, content)
            if len(ga_scripts) > 1:
                # Keep only the first one and ensure it's correct
                content = re.sub(ga_script_pattern, '', content)
                # Add it back once in the head
                if '<head>' in content:
                    correct_script = '<script async src="https://www.googletagmanager.com/gtag/js?id=G-J09TH92K0M"></script>'
                    content = content.replace('<head>', f'<head>\n    {correct_script}', 1)
                issues.append(f'Fixed {len(ga_scripts)} duplicate GA script tags')

            # 4. Ensure gtag config is correct and only appears once
            gtag_config_pattern = r'gtag\([\'"]config[\'"],\s*[\'"][^\'"]+[\'"]\)'
            gtag_configs = re.findall(gtag_config_pattern, content)
            if len(gtag_configs) > 1:
                # Remove all gtag configs
                content = re.sub(gtag_config_pattern, '', content)
                issues.append(f'Removed {len(gtag_configs)} duplicate gtag configs')

            # 5. Add analytics-config.js before </body> if not present
            if 'analytics-config.js' not in content and '</body>' in content:
                analytics_script = '    <script src="/analytics-config.js" defer></script>\n'
                content = content.replace('</body>', f'{analytics_script}</body>')
                issues.append('Added analytics-config.js')

            # 6. Clean up old event tracking scripts that are redundant
            old_tracking_patterns = [
                r'// Track affiliate clicks[\s\S]*?}\);[\s\n]*}\);',
                r'// Analytics tracking[\s\S]*?}\);[\s\n]*}\);',
                r'// Track scroll depth[\s\S]*?}\);[\s\n]*}\);'
            ]
            for pattern in old_tracking_patterns:
                if re.search(pattern, content, re.MULTILINE):
                    content = re.sub(pattern, '', content, flags=re.MULTILINE)
                    issues.append('Removed redundant tracking script')

            # Save if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_files.append(file_path)
                issues_found[file_path] = issues
                print(f'Fixed: {file_path}')
                for issue in issues:
                    print(f'  - {issue}')

        except Exception as e:
            print(f'Error processing {file_path}: {str(e)}')

    # Create a simplified GA initialization script
    ga_init = '''<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-J09TH92K0M"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  // Basic configuration - enhanced tracking in analytics-config.js
  gtag('config', 'G-J09TH92K0M', {
    'anonymize_ip': true
  });
</script>'''

    # Save the template for reference
    with open('GA_INIT_TEMPLATE.txt', 'w') as f:
        f.write(ga_init)

    print(f'\n=== Analytics Fix Summary ===')
    print(f'Total files processed: {len(html_files)}')
    print(f'Files fixed: {len(fixed_files)}')
    print(f'\nMost common issues:')

    issue_counts = {}
    for issues in issues_found.values():
        for issue in issues:
            issue_type = issue.split()[0] + ' ' + issue.split()[1] if len(issue.split()) > 1 else issue
            issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1

    for issue, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
        print(f'  - {issue}: {count} files')

    # Create recommendations
    recommendations = '''
=== Google Analytics Setup Recommendations ===

1. IMMEDIATE ACTIONS:
   - Review Google Analytics real-time reports to verify tracking
   - Set up custom dimensions in GA4 for page_type and content_category
   - Create audiences based on engagement metrics

2. GA4 CONFIGURATION:
   Go to your GA4 property and configure:

   a) Custom Dimensions (Admin > Custom definitions):
      - page_type (Event parameter)
      - content_category (Event parameter)
      - merchant (Event parameter)

   b) Enhanced Measurement (Admin > Data Streams > Web):
      - Enable all toggles (scrolls, outbound clicks, site search, etc.)

   c) Audiences (Admin > Audiences):
      - High-intent users (scroll > 75%, time > 60s)
      - Review readers (page_type = review)
      - Affiliate clickers (event = affiliate_click)

3. EVENTS TO MONITOR:
   Key events now being tracked:
   - affiliate_click (with merchant details)
   - internal_navigation (user flow)
   - scroll_depth (25%, 50%, 75%, 90%, 100%)
   - time_on_page (30s, 60s, 120s, 300s)
   - email_signup (form submissions)
   - search_query (site search)
   - Web Vitals (LCP, FID for performance)

4. REFERRAL TRACKING FIX:
   - Linker parameter added for cross-domain tracking
   - Add your domain to referral exclusion list in GA4

5. TESTING:
   - Use GA4 DebugView to see events in real-time
   - Install Google Analytics Debugger Chrome extension
   - Run: GATracking.debugMode(true) in browser console

6. ATTRIBUTION:
   The new setup tracks:
   - Which pages lead to affiliate clicks
   - User journey through your site
   - Content engagement patterns
   - Conversion paths
'''

    with open('GA_SETUP_RECOMMENDATIONS.txt', 'w') as f:
        f.write(recommendations)

    print('\nRecommendations saved to GA_SETUP_RECOMMENDATIONS.txt')
    print('GA initialization template saved to GA_INIT_TEMPLATE.txt')

if __name__ == '__main__':
    fix_analytics()