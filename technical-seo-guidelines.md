# Technical SEO Guidelines - Safe for Bulk Application

**PURPOSE**: These guidelines contain only non-breaking technical improvements that can be safely applied across all pages without affecting functionality or user experience.

## Meta Tag Standards (Safe Additions/Corrections)

### Required Meta Tags - Add if Missing
```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

### Title Tag Validation (Non-Breaking)
- Ensure title tags exist on all pages
- Verify titles are under 60 characters
- Check for duplicate title tags across pages
- Add title tags to pages missing them (use H1 content as fallback)

### Meta Description Validation
- Add meta descriptions to pages missing them
- Trim descriptions over 155 characters (don't remove, just flag for manual review)
- Ensure descriptions exist and are not empty

### Canonical URL Implementation
- Add canonical tags if missing: `<link rel="canonical" href="[current-page-url]">`
- Verify existing canonical URLs point to correct HTTPS version
- Fix relative canonical URLs to absolute URLs

## Open Graph Tags (Safe Additions)

Add these if missing (use existing meta description and title as fallbacks):
```html
<meta property="og:title" content="[page-title]">
<meta property="og:description" content="[meta-description]">
<meta property="og:url" content="[canonical-url]">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Shopify App Authority">
```

## Twitter Cards (Safe Additions)
```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="[page-title]">
<meta name="twitter:description" content="[meta-description]">
```

## Performance Optimizations (Non-Breaking)

### CSS Optimization
- Remove unused CSS declarations from inline styles
- Minify inline CSS (remove comments, extra whitespace)
- Consolidate duplicate CSS rules
- Add `font-display: swap;` to custom font declarations

### Image Optimization (Safe)
- Add missing `alt` attributes to images (use filename as fallback)
- Add `loading="lazy"` to images below the fold
- Ensure image dimensions are specified in HTML or CSS
- Add `decoding="async"` to non-critical images

### JavaScript Optimization
- Add `async` or `defer` to non-critical script tags
- Ensure external scripts use HTTPS
- Add error handling to inline JavaScript

## HTML Validation (Safe Fixes)

### Structure Validation
- Ensure proper DOCTYPE declaration exists
- Verify `<html lang="en">` attribute is set
- Check for unclosed HTML tags
- Remove or fix malformed HTML comments

### Accessibility Improvements (Non-Breaking)
- Add missing `alt` attributes to images
- Ensure form inputs have associated labels
- Add `rel="noopener"` to external links with `target="_blank"`
- Verify heading hierarchy (H1 -> H2 -> H3, no skipping levels)

### Link Optimization
- Convert HTTP links to HTTPS where possible
- Add `rel="nofollow"` to external links where appropriate
- Fix broken internal links (404 errors)
- Remove or update deprecated link attributes

## Schema Markup Validation (Non-Breaking)

### Existing Schema Fixes
- Validate JSON-LD syntax for errors
- Remove duplicate schema declarations
- Fix malformed schema properties
- Ensure proper schema nesting structure

### Safe Schema Additions
Only add if no existing schema conflicts:
```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "[page-title]",
  "description": "[meta-description]",
  "url": "[canonical-url]"
}
```

## Security Headers (Safe Additions)

### Content Security (Meta Tags)
- Add `<meta http-equiv="X-Content-Type-Options" content="nosniff">`
- Ensure referrer policy is set: `<meta name="referrer" content="strict-origin-when-cross-origin">`

### Link Security
- Add `rel="noopener noreferrer"` to external links
- Ensure social media links use `rel="nofollow"`

## Mobile Optimization (Non-Breaking)

### Responsive Design Validation
- Verify viewport meta tag is present and correct
- Check for horizontal scrolling issues in CSS
- Ensure touch targets are appropriately sized
- Validate mobile-friendly navigation

### Touch Interface
- Add appropriate `cursor: pointer` to interactive elements
- Ensure buttons have adequate touch target size (44px minimum)

## Analytics and Tracking (Safe)

### Google Analytics
- Verify gtag implementation is correct
- Check for duplicate tracking codes
- Ensure conversion tracking is properly implemented

### Privacy Compliance
- Verify cookie consent implementations don't break
- Check that tracking codes respect user preferences

## Sitemap and Robots (Safe Updates)

### Robots.txt Validation
- Ensure robots.txt exists and is properly formatted
- Verify no critical pages are accidentally blocked
- Check for syntax errors in robots directives

### XML Sitemap
- Validate sitemap.xml exists and is accessible
- Check sitemap URLs return 200 status codes
- Ensure lastmod dates are properly formatted

## Implementation Rules

### SAFE OPERATIONS ONLY
- Only ADD missing elements, never REMOVE existing content
- Only FIX broken markup, never change working functionality
- Only OPTIMIZE performance, never alter user experience
- Only VALIDATE data, never modify content meaning

### EXCLUSIONS (Manual Review Required)
- Do not modify H1 tags (affects content hierarchy)
- Do not change URL structures (breaks existing links)
- Do not alter existing schema that's working
- Do not modify navigation or menu structures
- Do not change image file names or paths

### TESTING REQUIREMENTS
- Validate HTML after changes
- Check for JavaScript errors in console
- Verify page still loads correctly
- Test mobile responsiveness maintained

### ROLLBACK PLAN
- Create backup of files before modification
- Test changes on staging environment first
- Document all changes made for easy reversal
- Monitor site performance after deployment

---

**COMMAND FOR CLAUDE CODE:**
"Apply these technical SEO guidelines to all HTML files. Focus only on safe, non-breaking improvements. Create backup branch before executing."