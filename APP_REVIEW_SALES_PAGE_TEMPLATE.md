# App Review Sales Page Template

## Overview
This template documents the UPDATED format used for Judge.me, Postscript, Okendo, Stamped.io, Rebuy, and Attentive review pages - a modern, mobile-optimized sales page format for individual app reviews. This format replaces the original Klaviyo-style template with improved design and responsiveness.

## Page Structure (MUST FOLLOW THIS EXACT ORDER)

### 1. HTML Head Section
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[App Name] Review 2025: [Compelling Value Prop with Specific Benefit]</title>
    <meta name="description" content="Complete [App Name] review from $100M+ ad spend experience. [Specific benefit like 'Setup guide, pricing analysis, and advanced strategies that drive X% results'].">
    <link rel="canonical" href="https://shopifyappauthority.com/[app-slug]-review/">
    <meta property="og:title" content="[App Name] Review 2025: [Value Prop]">
    <meta property="og:description" content="Complete [App Name] review from someone who's actually used it to [specific achievement].">
    <meta property="og:url" content="https://shopifyappauthority.com/[app-slug]-review/">
    <meta property="og:type" content="article">

    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-J09TH92K0M"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-J09TH92K0M');
    </script>

    <!-- Facebook Pixel -->
    <script>
        !function(f,b,e,v,n,t,s)
        {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)}(window, document,'script',
        'https://connect.facebook.net/en_US/fbevents.js');
        fbq('init', '1087447432711058');
        fbq('track', 'PageView');
    </script>
```

### 2. Navigation (Mobile-First Design)
- Clean, modern navigation with consistent styling
- Logo with rocket emoji: `🚀&nbsp;ShopifyAppAuthority`
- Dropdown menus for Categories and Store Size
- **Mobile-first responsive design** with hamburger menu toggle
- Smooth transitions and hover effects

### 3. Breadcrumb
```html
<div class="breadcrumb">
    <div class="container">
        <a href="/">Home</a>
        <span>›</span>
        <a href="/app-categories/">Categories</a>
        <span>›</span>
        <span>[App Name] Review</span>
    </div>
</div>
```

### 4. Hero Section (CRITICAL - MUST BE COMPELLING)
```html
<div class="hero">
    <div class="container">
        <h1>[App Name]: [Compelling Tagline That Promises Specific Value]</h1>
        <p class="subtitle">Complete review from someone who's [specific credibility statement with numbers]</p>
        <a href="[affiliate-link]" class="hero-cta" target="_blank">Start Your Free [App Name] Trial →</a>
    </div>
</div>
```

**Hero Formula:**
- **H1**: App name + specific value proposition
- **Subtitle**: Authority statement with specific numbers ($X managed, Y years experience)
- **CTA**: Action-oriented with urgency

**Examples:**
- "ReCharge: The Subscription App That Triples Customer LTV"
- "Gorgias: Cut Support Response Time by 70% While Increasing Sales"
- "Triple Whale: See Your Real Profit in Real-Time"

### 5. Pain Section (CREATE URGENCY)
```html
<div class="pain-section">
    <h2>🔥 [Urgent Problem Statement]</h2>
    <p>[Describe the pain of not using this app. What are competitors doing while they're not? What money/opportunity are they losing? Be specific and create FOMO.]</p>
</div>
```

**Pain Formula:**
- Start with action verb: "Stop losing...", "Stop wasting...", "Stop letting..."
- Reference competitors gaining advantage
- Specific consequences of inaction
- Create urgency and FOMO

### 6. Statistics Grid (3 KEY METRICS)
```html
<div class="stats-grid">
    <div class="stat-card">
        <span class="stat-number">[Number]%</span>
        <span class="stat-label">[Specific metric improvement]</span>
    </div>
    <div class="stat-card">
        <span class="stat-number">[Multiplier]x</span>
        <span class="stat-label">[Comparison vs alternatives]</span>
    </div>
    <div class="stat-card">
        <span class="stat-number">[Price/Value]</span>
        <span class="stat-label">[Accessibility statement]</span>
    </div>
</div>
```

**Stat Guidelines:**
- First stat: Primary benefit (percentage improvement)
- Second stat: Competitive advantage (X times better)
- Third stat: Accessibility (FREE trial, low cost, etc.)

### 7. Features Section (6 FEATURE CARDS - CLEAN DESIGN)
```html
<section class="features-section">
    <div class="container">
        <div class="section-header">
            <h2>Why [App Name] Dominates [Category]</h2>
            <p>After testing every major [category] platform, here's why [App Name] consistently outperforms the competition</p>
        </div>

        <div class="feature-grid">
            <div class="feature-card">
                <h3><span class="feature-icon">[Emoji]</span> [Feature Title]</h3>
                <ul>
                    <li><strong>[Key benefit]</strong> [specific explanation]</li>
                    <li><strong>[Key benefit]</strong> [specific explanation]</li>
                    <li><strong>[Key benefit]</strong> [specific explanation]</li>
                    <li><strong>[Key benefit]</strong> [specific explanation]</li>
                </ul>
            </div>
            <!-- Repeat for 6 total feature cards -->
        </div>
    </div>
</section>
```

### Feature Cards CSS (UPDATED CLEAN DESIGN):
```css
.feature-card {
    background: white;  /* CHANGED: Clean white background */
    border: 2px solid #10b981;  /* UPDATED: Consistent green border */
    border-radius: 12px;
    padding: 2rem;
}

.feature-card h3 {
    color: #1f2937;  /* UPDATED: Consistent text color */
    margin-bottom: 1rem;
    font-size: 1.3rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.feature-icon {
    font-size: 1.5rem;  /* UPDATED: Consistent icon size */
}

.feature-card ul {
    list-style: none;
}

.feature-card li {
    margin-bottom: 0.75rem;
    color: #4b5563;  /* UPDATED: Consistent text color */
    line-height: 1.5;
}

.feature-card strong {
    color: #1f2937;  /* UPDATED: Consistent bold color */
}
```

**Feature Icons by Category:**
- 🤖 AI/Automation features
- 📧 Communication features
- 💰 Revenue/Financial features
- 🎨 Design/Creative features
- 📱 Mobile/Omnichannel features
- 🔗 Integration features
- 📊 Analytics/Data features
- ⚡ Speed/Performance features
- 🛡️ Security features
- 🎯 Targeting features

### 8. Pros and Cons Section (HONEST ASSESSMENT)
```html
<div class="pros-cons">
    <div class="pros">
        <h3>✅ What We Love About [App Name]</h3>
        <ul>
            <li><strong>[Pro headline]</strong> [specific detail]</li>
            <li><strong>[Pro headline]</strong> [specific detail]</li>
            <!-- 5-7 pros total -->
        </ul>
    </div>

    <div class="cons">
        <h3>❌ Potential Drawbacks</h3>
        <ul>
            <li><strong>[Con headline]</strong> [honest limitation]</li>
            <li><strong>[Con headline]</strong> [honest limitation]</li>
            <!-- 3-5 cons total -->
        </ul>
    </div>
</div>
```

**Rules:**
- Always include real drawbacks for credibility
- Bold the main point, explain in detail
- Pros should outnumber cons
- Be honest but frame cons as minor compared to value

### 9. Setup Section (5-STEP PROCESS)
```html
<section class="setup-section">
    <div class="section-header">
        <h2>How to Get Started with [App Name]</h2>
        <p>Follow this proven setup process to [specific outcome from day one]</p>
    </div>

    <div class="setup-steps">
        <div class="setup-step">
            <div class="step-number">1</div>
            <h3>[Step Title]</h3>
            <p>[Specific instructions with timing and expected outcome]</p>
        </div>
        <!-- Repeat for 5 steps total -->
    </div>
</section>
```

**Setup Steps Framework:**
1. **Account Creation / Installation** - Quick setup with timing expectations
2. **Initial Configuration / Integration** - Core platform connection
3. **Feature Implementation** - Key features that drive results
4. **Optimization Setup** - Performance and targeting configuration
5. **Launch and Scale** - Go-live with monitoring and optimization

### Setup Section CSS (Required):
```css
.setup-section {
    background: white;
    padding: 4rem 0;
}

.setup-steps {
    display: grid;
    gap: 2rem;
    max-width: 800px;
    margin: 0 auto;
}

.setup-step {
    background: #f8fafc;
    padding: 2rem;
    border-radius: 12px;
    border-left: 4px solid #7c3aed;
    display: flex;
    gap: 1.5rem;
    align-items: flex-start;
}

.step-number {
    background: #7c3aed;
    color: white;
    width: 3rem;
    height: 3rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 1.2rem;
    flex-shrink: 0;
}
```

### 10. Testimonial Section
```html
<div class="testimonial-section">
    <div class="testimonial">
        <blockquote>"[Specific result-focused testimonial that mentions numbers and timeframe]"</blockquote>
        <div class="testimonial-author">— [Name], [Title] of [Company] ([Revenue/Size indicator])</div>
    </div>
</div>
```

**Testimonial Formula:**
- Specific results with numbers
- Timeframe for results
- Before/after comparison
- Company size/revenue for context

### 11. Pricing Section (3-TIER GRID)
```html
<section class="pricing-section">
    <div class="container">
        <div class="section-header">
            <h2>[App Name] Pricing: [Value Prop About Pricing]</h2>
            <p>[Explanation of pricing model]</p>
        </div>

        <div class="pricing-grid">
            <div class="pricing-card">
                <h3>[Plan Name]</h3>
                <div class="price">$[X]<span class="price-period">/month</span></div>
                <ul class="pricing-features">
                    <li><strong>[Key feature]</strong></li>
                    <!-- 5-7 features -->
                </ul>
                <a href="[affiliate-link]" class="cta-button secondary" target="_blank">[CTA Text]</a>
            </div>

            <div class="pricing-card featured">
                <div class="pricing-badge">Most Popular</div>
                <h3>[Plan Name]</h3>
                <!-- Same structure -->
            </div>

            <div class="pricing-card">
                <h3>[Plan Name]</h3>
                <!-- Same structure -->
            </div>
        </div>

        <p style="text-align: center; margin-top: 2rem; opacity: 0.8;">[Additional pricing note]</p>
    </div>
</section>
```

### 12. Final CTA Section (CLOSING THE SALE)
```html
<div class="container">
    <div class="final-cta-section">
        <h2>Ready to [Desired Outcome]?</h2>
        <p>[Social proof statement with specific numbers]</p>
        <a href="[affiliate-link]" class="final-cta" target="_blank">Start Your Free [App Name] Trial Now →</a>
        <p style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">[Risk reversal statement • Key benefit • Time to value]</p>
    </div>
</div>
```

### 13. Tracking Scripts
```javascript
// Mobile menu toggle
document.querySelector('.mobile-menu-toggle').addEventListener('click', function() {
    document.querySelector('.nav-links').classList.toggle('active');
});

// Track CTA clicks
document.querySelectorAll('a[href*="[app-domain]"]').forEach(function(link) {
    link.addEventListener('click', function() {
        gtag('event', 'click', {
            'event_category': 'CTA',
            'event_label': '[App Name] Review Page',
            'value': 1
        });

        fbq('track', 'Lead', {
            content_name: '[App Name] Review CTA',
            content_category: '[Category]'
        });
    });
});
```

## CSS Classes (MUST INCLUDE ALL)

### Required Style Classes
- `.hero` - Gradient purple background
- `.hero-cta` - Green gradient CTA button
- `.pain-section` - Red gradient warning box
- `.stat-card` - Green gradient stat boxes
- `.feature-card` - Green border feature boxes
- `.pros` - Green gradient for pros
- `.cons` - Red gradient for cons
- `.setup-step` - Gray background with step numbers
- `.pricing-card` - Transparent cards on purple
- `.pricing-card.featured` - Green border for popular plan
- `.final-cta-section` - Green gradient closing CTA
- `.cta-button` - Standard green gradient button
- `.cta-button.secondary` - Transparent secondary button

## Content Guidelines

### Tone and Voice
- **Urgent and direct** - Create FOMO from the start
- **Authority-based** - Reference $100M+ ad spend, years of experience
- **Brutally honest** - Include real drawbacks for credibility
- **Benefit-focused** - Always lead with what's in it for them
- **Specific numbers** - Use exact metrics, not vague claims

### SEO Optimization
- App name in title, H1, and 5+ times naturally
- Long-tail keywords in section headers
- Category keywords throughout
- "Review 2025" for temporal relevance
- Specific feature names for search

### Conversion Elements
- Minimum 5 CTAs throughout the page
- Progressive CTAs with different angles
- Social proof with specific numbers
- Risk reversal statements
- Urgency and scarcity where applicable

### Compliance Rules
- ✅ Real testimonials only (or clearly marked as examples)
- ✅ Accurate pricing information
- ✅ Honest pros and cons
- ✅ FTC compliant affiliate disclosure
- ❌ NO fake countdown timers
- ❌ NO fabricated statistics
- ❌ NO false scarcity
- ❌ NO misleading claims

## Quality Checklist

Before publishing, verify:

### Structure
- [ ] All 13 sections present in correct order
- [ ] Breadcrumb navigation correct
- [ ] Mobile responsive design
- [ ] All CTAs have affiliate links
- [ ] Tracking scripts installed

### Content
- [ ] Compelling hero headline with specific value
- [ ] Pain section creates urgency
- [ ] 3 impressive statistics
- [ ] 6 detailed feature cards
- [ ] Honest pros and cons
- [ ] 5-step setup guide
- [ ] Testimonial with specific results
- [ ] 3-tier pricing grid
- [ ] Strong final CTA

### SEO
- [ ] Title tag optimized
- [ ] Meta description compelling
- [ ] App name mentioned 5+ times
- [ ] All images have alt text
- [ ] Canonical URL set

### Tracking
- [ ] Google Analytics configured
- [ ] Facebook Pixel installed
- [ ] CTA click tracking working
- [ ] Affiliate links tagged properly

## File Naming Convention

```
/[app-slug]-review/index.html
```

Examples:
- `/klaviyo-review/index.html`
- `/recharge-review/index.html`
- `/gorgias-review/index.html`
- `/triple-whale-review/index.html`

## When to Use This Template

Use this template for:
- ✅ Individual app deep-dive review pages
- ✅ App comparison pages (adapt for 2-3 apps)
- ✅ Category leader spotlight pages
- ✅ "Is [App] Worth It?" pages

Do NOT use for:
- ❌ Listicle pages (use LISTICLE_ENTRY_TEMPLATE.md)
- ❌ Category overview pages
- ❌ Blog posts or guides
- ❌ Policy pages

## Mobile Responsiveness (CRITICAL)

### Required Mobile CSS:
```css
@media (max-width: 768px) {
    .hero h1 {
        font-size: 2rem;
    }

    .pros-cons {
        grid-template-columns: 1fr;
    }

    .pricing-grid {
        grid-template-columns: 1fr;
    }

    .pricing-card.featured {
        transform: none;
    }

    .setup-step {
        flex-direction: column;
        align-items: center;
        text-align: center;
        gap: 1rem;
        padding: 1.5rem;
    }

    .setup-step .step-number {
        margin-bottom: 0.5rem;
    }

    .container {
        padding: 0 15px;
    }
}
```

### Mobile Optimization Requirements:
- **Responsive navigation** with working hamburger menu
- **Stacked layouts** for pros/cons and pricing on mobile
- **Centered setup steps** with proper spacing
- **Touch-friendly buttons** with adequate sizing
- **Readable text sizes** at all screen widths

## Success Metrics

This UPDATED format is optimized for:
- **Conversion Rate**: 6-10% to affiliate click (improved vs old format)
- **Time on Page**: 4-6 minutes average (increased engagement)
- **Scroll Depth**: 75%+ to final CTA (better flow)
- **Bounce Rate**: Under 35% (improved mobile experience)
- **Mobile Conversion**: 65%+ of desktop rate (mobile-first design)

**Last Updated:** January 2025
**Based on:** Judge.me, Postscript, Okendo, Stamped.io, Rebuy, Attentive performance
**Next Review:** After implementing across all review pages