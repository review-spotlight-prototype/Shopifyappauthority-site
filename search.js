// Search functionality for Shopify App Authority
const searchIndex = [
    // Email Marketing Reviews
    { title: "Moosend Review", url: "/moosend-review/", type: "review", category: "Email Marketing", keywords: ["email", "marketing", "automation", "moosend", "email campaigns"] },
    { title: "Klaviyo Review", url: "/klaviyo-review/", type: "review", category: "Email Marketing", keywords: ["klaviyo", "email", "marketing", "ecommerce", "automation"] },
    { title: "ActiveCampaign Review", url: "/activecampaign-review/", type: "review", category: "Email Marketing", keywords: ["activecampaign", "email", "marketing", "crm", "automation"] },
    { title: "AWeber Review", url: "/aweber-review/", type: "review", category: "Email Marketing", keywords: ["aweber", "email", "marketing", "autoresponder"] },
    { title: "GetResponse Review", url: "/getresponse-review/", type: "review", category: "Email Marketing", keywords: ["getresponse", "email", "marketing", "landing pages", "webinars"] },
    { title: "Constant Contact Review", url: "/constant-contact-review/", type: "review", category: "Email Marketing", keywords: ["constant contact", "email", "marketing", "small business"] },
    { title: "MailerLite Review", url: "/mailerlite-review/", type: "review", category: "Email Marketing", keywords: ["mailerlite", "email", "marketing", "free", "automation"] },
    { title: "Mailchimp Review", url: "/mailchimp-review/", type: "review", category: "Email Marketing", keywords: ["mailchimp", "email", "marketing", "newsletter", "automation"] },
    { title: "Omnisend Review", url: "/omnisend-review/", type: "review", category: "Email Marketing", keywords: ["omnisend", "email", "sms", "marketing", "ecommerce"] },

    // SMS Marketing Reviews
    { title: "Postscript Review", url: "/postscript-review/", type: "review", category: "SMS Marketing", keywords: ["postscript", "sms", "text", "marketing", "abandoned cart"] },

    // CRM & Sales Reviews
    { title: "HubSpot Review", url: "/hubspot-review/", type: "review", category: "CRM", keywords: ["hubspot", "crm", "sales", "marketing hub", "inbound"] },
    { title: "ClickFunnels Review", url: "/clickfunnels-review/", type: "review", category: "Sales Funnels", keywords: ["clickfunnels", "sales funnels", "landing pages", "conversions"] },

    // Popup & Conversion Reviews
    { title: "Justuno Review", url: "/justuno-review/", type: "review", category: "Popups", keywords: ["justuno", "popups", "conversion", "exit intent", "email capture"] },

    // Listicles & Guides
    { title: "Best Email Marketing Apps for Shopify", url: "/best-shopify-apps-email-marketing/", type: "listicle", category: "Email Marketing", keywords: ["best", "email", "marketing", "apps", "shopify", "comparison"] },
    { title: "Best Shopify Apps 2025", url: "/best-shopify-apps-2025/", type: "listicle", category: "All Categories", keywords: ["best", "shopify", "apps", "2025", "ultimate guide"] },
    { title: "Best CRM & Sales Apps", url: "/best-shopify-apps-crm-sales/", type: "listicle", category: "CRM", keywords: ["best", "crm", "sales", "apps", "shopify"] },
    { title: "Best Shopify Upsell Apps", url: "/best-shopify-upsell-apps/", type: "listicle", category: "Sales", keywords: ["upsell", "cross-sell", "aov", "average order value"] },
    { title: "Free Shopify Apps", url: "/free-shopify-apps/", type: "listicle", category: "Free Apps", keywords: ["free", "shopify", "apps", "budget", "no cost"] },

    // Alternative Pages
    { title: "Klaviyo Alternatives", url: "/klaviyo-alternatives/", type: "alternatives", category: "Email Marketing", keywords: ["klaviyo", "alternatives", "competitors", "email", "marketing"] },
    { title: "Zendesk Alternatives", url: "/zendesk-alternatives/", type: "alternatives", category: "Customer Support", keywords: ["zendesk", "alternatives", "customer support", "helpdesk"] },

    // Category Pages
    { title: "Shopify Email Marketing", url: "/shopify-email-marketing/", type: "category", category: "Email Marketing", keywords: ["email", "marketing", "shopify", "category", "overview"] },
    { title: "Klaviyo for Shopify", url: "/klaviyo-shopify/", type: "guide", category: "Email Marketing", keywords: ["klaviyo", "shopify", "integration", "setup", "guide"] },

    // Store Size Guide
    { title: "Apps by Store Size", url: "/store-size/", type: "guide", category: "All Categories", keywords: ["store size", "small", "medium", "enterprise", "recommendations"] },

    // Blog Posts
    { title: "Moosend AI Email Marketing", url: "/blog/moosend-ai-email-marketing/", type: "blog", category: "Email Marketing", keywords: ["moosend", "ai", "artificial intelligence", "email", "blog"] },
    { title: "Kit (ConvertKit) for Shopify", url: "/blog/kit-convertkit-shopify-email-marketing/", type: "blog", category: "Email Marketing", keywords: ["kit", "convertkit", "creators", "email", "blog"] },
    { title: "GetResponse vs Klaviyo", url: "/blog/getresponse-vs-klaviyo-budget-alternative/", type: "blog", category: "Email Marketing", keywords: ["getresponse", "klaviyo", "comparison", "budget", "blog"] },
    { title: "Constant Contact 30 Year Veteran", url: "/blog/constant-contact-30-year-veteran/", type: "blog", category: "Email Marketing", keywords: ["constant contact", "veteran", "experience", "blog"] },
    { title: "AWeber Veteran Email Marketing", url: "/blog/aweber-veteran-email-marketing/", type: "blog", category: "Email Marketing", keywords: ["aweber", "veteran", "experience", "blog"] },
    { title: "ActiveCampaign Shopify Email", url: "/blog/activecampaign-shopify-email-marketing/", type: "blog", category: "Email Marketing", keywords: ["activecampaign", "shopify", "integration", "blog"] },
    { title: "MailerLite Free Forever", url: "/blog/mailerlite-free-forever-shopify/", type: "blog", category: "Email Marketing", keywords: ["mailerlite", "free", "forever", "blog"] },

    // Main Guides
    { title: "Building Shopify Empire Guide", url: "/building-shopify-empire-guide.html", type: "guide", category: "Strategy", keywords: ["building", "empire", "shopify", "strategy", "growth"] },

    // Payroll & HR
    { title: "Gusto Payroll Review - First Employee", url: "/blog/gusto-payroll-first-employee/", type: "blog", category: "Payroll & HR", keywords: ["gusto", "payroll", "first employee", "hr", "hiring", "payroll software", "small business"] }
];

class SiteSearch {
    constructor() {
        this.searchInput = null;
        this.searchResults = null;
        this.searchOverlay = null;
        this.isOpen = false;
        this.init();
    }

    init() {
        this.createSearchElements();
        this.attachEventListeners();
    }

    createSearchElements() {
        // Create search button for header
        const searchButton = document.createElement('button');
        searchButton.className = 'search-button';
        searchButton.innerHTML = '🔍';
        searchButton.setAttribute('aria-label', 'Search');

        // Create search overlay
        const overlay = document.createElement('div');
        overlay.className = 'search-overlay';
        overlay.innerHTML = `
            <div class="search-modal">
                <div class="search-header">
                    <input type="text" class="search-input" placeholder="Search for apps, reviews, guides..." autocomplete="off">
                    <button class="search-close" aria-label="Close search">✕</button>
                </div>
                <div class="search-filters">
                    <button class="filter-btn active" data-filter="all">All</button>
                    <button class="filter-btn" data-filter="review">Reviews</button>
                    <button class="filter-btn" data-filter="listicle">Best Of</button>
                    <button class="filter-btn" data-filter="guide">Guides</button>
                    <button class="filter-btn" data-filter="blog">Blog</button>
                </div>
                <div class="search-results"></div>
            </div>
        `;

        // Add to DOM
        document.body.appendChild(overlay);

        // Find header nav and add search button
        const nav = document.querySelector('.site-nav');
        if (nav) {
            // Insert search button before mobile menu toggle or at the end
            const mobileToggle = nav.querySelector('.mobile-menu-toggle');
            if (mobileToggle) {
                nav.insertBefore(searchButton, mobileToggle);
            } else {
                nav.appendChild(searchButton);
            }
        }

        // Store references
        this.searchButton = searchButton;
        this.searchOverlay = overlay;
        this.searchInput = overlay.querySelector('.search-input');
        this.searchResults = overlay.querySelector('.search-results');
        this.searchClose = overlay.querySelector('.search-close');
        this.filterButtons = overlay.querySelectorAll('.filter-btn');
    }

    attachEventListeners() {
        // Open search
        this.searchButton?.addEventListener('click', () => this.openSearch());

        // Close search
        this.searchClose?.addEventListener('click', () => this.closeSearch());
        this.searchOverlay?.addEventListener('click', (e) => {
            if (e.target === this.searchOverlay) {
                this.closeSearch();
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Cmd/Ctrl + K to open search
            if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                e.preventDefault();
                this.openSearch();
            }
            // Escape to close
            if (e.key === 'Escape' && this.isOpen) {
                this.closeSearch();
            }
        });

        // Search input
        this.searchInput?.addEventListener('input', (e) => {
            this.performSearch(e.target.value);
        });

        // Filter buttons
        this.filterButtons?.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.filterButtons.forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.performSearch(this.searchInput.value);
            });
        });
    }

    openSearch() {
        this.isOpen = true;
        this.searchOverlay.classList.add('active');
        this.searchInput.focus();
        document.body.style.overflow = 'hidden';

        // Show popular/recent searches initially
        this.showInitialContent();
    }

    closeSearch() {
        this.isOpen = false;
        this.searchOverlay.classList.remove('active');
        document.body.style.overflow = '';
        this.searchInput.value = '';
        this.searchResults.innerHTML = '';
    }

    showInitialContent() {
        const popularSearches = [
            { title: "Best Email Marketing Apps", url: "/best-shopify-apps-email-marketing/", type: "listicle" },
            { title: "Klaviyo Review", url: "/klaviyo-review/", type: "review" },
            { title: "Free Shopify Apps", url: "/free-shopify-apps/", type: "listicle" },
            { title: "Apps by Store Size", url: "/store-size/", type: "guide" },
            { title: "Moosend Review", url: "/moosend-review/", type: "review" }
        ];

        let html = '<div class="initial-content">';
        html += '<h3>Popular Searches</h3>';
        html += '<div class="search-items">';

        popularSearches.forEach(item => {
            html += this.createResultItem(item);
        });

        html += '</div></div>';
        this.searchResults.innerHTML = html;
    }

    performSearch(query) {
        if (!query || query.length < 2) {
            this.showInitialContent();
            return;
        }

        const activeFilter = document.querySelector('.filter-btn.active')?.dataset.filter || 'all';
        const searchTerms = query.toLowerCase().split(' ');

        // Search and score results
        let results = searchIndex.map(item => {
            let score = 0;
            const titleLower = item.title.toLowerCase();
            const keywordsStr = item.keywords.join(' ');

            searchTerms.forEach(term => {
                // Title exact match (highest priority)
                if (titleLower === term) score += 100;
                // Title contains term
                else if (titleLower.includes(term)) score += 50;
                // Title starts with term
                if (titleLower.startsWith(term)) score += 25;
                // Keywords contain term
                if (keywordsStr.includes(term)) score += 10;
                // Category matches
                if (item.category.toLowerCase().includes(term)) score += 15;
                // Type matches
                if (item.type.toLowerCase().includes(term)) score += 5;
            });

            return { ...item, score };
        });

        // Filter by type if not "all"
        if (activeFilter !== 'all') {
            results = results.filter(item => item.type === activeFilter);
        }

        // Filter out zero scores and sort
        results = results
            .filter(item => item.score > 0)
            .sort((a, b) => b.score - a.score)
            .slice(0, 10); // Limit to top 10 results

        // Display results
        this.displayResults(results, query);
    }

    displayResults(results, query) {
        if (results.length === 0) {
            this.searchResults.innerHTML = `
                <div class="no-results">
                    <p>No results found for "<strong>${this.escapeHtml(query)}</strong>"</p>
                    <p class="suggestion">Try searching for: email marketing, shopify apps, or review</p>
                </div>
            `;
            return;
        }

        let html = '<div class="search-items">';
        results.forEach(item => {
            html += this.createResultItem(item);
        });
        html += '</div>';

        this.searchResults.innerHTML = html;
    }

    createResultItem(item) {
        const typeIcon = {
            review: '⭐',
            listicle: '📋',
            guide: '📖',
            blog: '📝',
            alternatives: '🔄',
            category: '📁'
        };

        const typeLabel = {
            review: 'Review',
            listicle: 'Best Of',
            guide: 'Guide',
            blog: 'Blog',
            alternatives: 'Alternatives',
            category: 'Category'
        };

        return `
            <a href="${item.url}" class="search-item">
                <span class="search-icon">${typeIcon[item.type] || '📄'}</span>
                <div class="search-content">
                    <div class="search-title">${this.escapeHtml(item.title)}</div>
                    <div class="search-meta">
                        <span class="search-type">${typeLabel[item.type] || item.type}</span>
                        <span class="search-category">${item.category}</span>
                    </div>
                </div>
            </a>
        `;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize search when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.siteSearch = new SiteSearch();
    });
} else {
    window.siteSearch = new SiteSearch();
}