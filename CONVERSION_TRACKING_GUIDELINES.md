# Conversion Tracking Guidelines for Claude Code

## UTM Parameter Standards

### Campaign Structure
- **Source**: Always use "shopifyappauthority.com"
- **Medium**: "affiliate-review", "comparison-page", "category-hub"
- **Campaign**: App name (e.g., "klaviyo", "recharge", "gorgias")
- **Content**: Page section (e.g., "top-cta", "bottom-cta", "pricing-table")
- **Term**: Specific placement (e.g., "hero-button", "pros-section")

### URL Format Examples
```
https://partner.app.com/signup?utm_source=shopifyappauthority&utm_medium=affiliate-review&utm_campaign=klaviyo&utm_content=hero-cta&utm_term=free-trial-button
```

## Google Analytics Goal Setup

### Event Tracking Standards
- **Affiliate Click**: Category "Affiliate", Action "Click", Label "[App Name]"
- **Email Signup**: Category "Lead", Action "Subscribe", Label "Newsletter"
- **Form Submit**: Category "Engagement", Action "Contact", Label "Contact Form"
- **Resource Download**: Category "Content", Action "Download", Label "[Resource Name]"

### Custom Events
```javascript
gtag('event', 'affiliate_click', {
  'app_name': 'klaviyo',
  'placement': 'hero_cta',
  'page_url': window.location.href
});
```

## CTA Button Tracking

### Button Identification System
- **Primary CTA**: Main action button (free trial, pricing)
- **Secondary CTA**: Supporting actions (learn more, compare)
- **Tertiary CTA**: Navigation or informational links

### A/B Testing Framework
- Test button colors: primary brand vs. contrasting colors
- Test button text: "Free Trial" vs. "Start Free" vs. "Try Now"
- Test placement: top vs. middle vs. bottom of page
- Test urgency: "Start Today" vs. "Limited Time" vs. neutral

### Performance Metrics
- Click-through rate by button type and placement
- Conversion rate from click to signup
- Revenue attribution per traffic source
- Cost per acquisition by content type

## Affiliate Link Management

### Link Structure Standards
- Use consistent affiliate parameter formats
- Include tracking identifiers for source attribution
- Maintain backup links if primary affiliate fails
- Document all affiliate relationships and commission rates

### Revenue Attribution
- Track first click vs. last click attribution
- Monitor assisted conversions from multiple touchpoints
- Calculate lifetime value impact of content types
- Measure cross-selling success between app recommendations

## Heat Mapping and User Behavior

### Implementation Requirements
- Track scroll depth on all review pages
- Monitor click patterns on comparison tables
- Analyze time spent on pricing sections
- Record form abandonment rates

### Optimization Triggers
- If scroll depth <50%, review content structure
- If CTA clicks <2%, test button placement/design
- If form abandonment >70%, simplify lead capture
- If time on page <2 minutes, improve content engagement

## Content Performance Metrics

### Page-Level KPIs
- **Traffic Quality**: Source, bounce rate, session duration
- **Engagement**: Pages per session, return visitor rate
- **Conversion**: Email signups, affiliate clicks, form submissions
- **Revenue**: Commission tracking, customer lifetime value

### Content Type Analysis
- Individual reviews vs. comparison pages conversion rates
- Category hub performance vs. specific app pages
- Long-form vs. concise content effectiveness
- Video/interactive content vs. text-only performance

## Mobile Conversion Tracking

### Mobile-Specific Metrics
- Mobile vs. desktop conversion rate differences
- Touch interaction patterns and heat maps
- Mobile form completion rates
- App store redirect success rates

### Mobile Optimization Alerts
- If mobile conversion rate <70% of desktop, investigate UX issues
- Monitor mobile page load times and performance scores
- Track mobile navigation usage and abandonment points

## Competitive Intelligence Tracking

### Competitor Monitoring
- Track competitor mention click-through rates
- Monitor search ranking changes for competitive terms
- Analyze backlink acquisition from comparison content
- Measure brand mention growth in industry discussions

## Reporting Automation

### Daily Dashboards
- Affiliate click volume and conversion rates
- Top-performing content and traffic sources
- Email list growth and engagement metrics
- Revenue attribution by content type

### Weekly Analysis
- Content performance trends and optimization opportunities
- Affiliate program performance comparison
- SEO ranking changes and traffic impact
- Competitor activity and market positioning shifts

### Monthly Reviews
- ROI analysis by content investment
- Customer acquisition cost trends
- Lifetime value projections and improvements
- Strategic recommendations for content expansion

## Data Privacy Compliance

### Analytics Implementation
- Respect user privacy preferences and consent
- Implement proper data retention policies
- Ensure GDPR/CCPA compliance in tracking
- Maintain transparency in data collection practices

### Affiliate Disclosure Tracking
- Monitor disclosure visibility and compliance
- Track user engagement with disclosure information
- Ensure proper attribution in all affiliate relationships
- Maintain documentation for regulatory compliance