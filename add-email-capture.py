import os
import re

def add_email_capture_script():
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk('.'):
        # Skip node_modules and other unnecessary directories
        if 'node_modules' in root or '.git' in root:
            continue
        for file in files:
            if file.endswith('.html') and file != 'building-shopify-empire-guide.html':
                html_files.append(os.path.join(root, file))

    updated_files = []
    skipped_files = []

    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if email-capture.js is already included
            if 'email-capture.js' in content:
                skipped_files.append(file_path)
                continue

            # Find the </body> tag and add the script before it
            if '</body>' in content:
                # Add the script right before </body>
                new_content = content.replace(
                    '</body>',
                    '    <script src="/email-capture.js" defer></script>\n</body>'
                )

                # Write the updated content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                updated_files.append(file_path)
                print(f'Updated: {file_path}')

        except Exception as e:
            print(f'Error processing {file_path}: {str(e)}')

    print(f'\nSummary:')
    print(f'Updated {len(updated_files)} files')
    print(f'Skipped {len(skipped_files)} files (already have email-capture.js)')
    print(f'Total HTML files processed: {len(html_files)}')

if __name__ == '__main__':
    add_email_capture_script()