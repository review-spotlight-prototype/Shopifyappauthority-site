#!/bin/bash

# Script to update navigation menus across all HTML files
# Adds Analytics & Attribution dropdown category

# Find all HTML files with navigation
files=$(rg -l "By Store Size" --type html | grep -v "MASTER_NAVIGATION_TEMPLATE.html" | grep -v "^index.html$")

for file in $files; do
    echo "Updating navigation in: $file"

    # Use sed to replace the navigation pattern
    sed -i 's|<li class="dropdown">.*<a href="/store-size/">By Store Size</a>|<li class="dropdown">\n                    <a href="/best-shopify-apps-analytics-attribution/">Analytics \& Attribution</a>\n                    <div class="dropdown-content">\n                        <a href="/hotjar-review/">Hotjar Review</a>\n                        <a href="/crazy-egg-review/">Crazy Egg Review</a>\n                        <a href="/google-analytics-360-review/">Google Analytics 360 Review</a>\n                        <a href="/mixpanel-review/">Mixpanel Review</a>\n                        <a href="/kissmetrics-review/">Kissmetrics Review</a>\n                    </div>\n                </li>\n                <li class="dropdown">\n                    <a href="/store-size/">By Store Size</a>|' "$file"
done

echo "Navigation update complete!"