// Centralized Google Analytics Configuration
// Tracks: Referral, Source, Medium, Keywords + Specific Click Events

(function() {
    // Configuration
    const GA_ID = 'G-J09TH92K0M';
    const DEBUG_MODE = false; // Set to true to see tracking events in console

    // Only initialize if gtag is loaded
    if (typeof gtag === 'undefined') {
        console.warn('Google Analytics not loaded');
        return;
    }

    // Get UTM and referral data
    const urlParams = new URLSearchParams(window.location.search);
    const utmData = {
        'campaign_source': urlParams.get('utm_source') || urlParams.get('source') || '',
        'campaign_medium': urlParams.get('utm_medium') || urlParams.get('medium') || '',
        'campaign_name': urlParams.get('utm_campaign') || '',
        'campaign_term': urlParams.get('utm_term') || urlParams.get('keyword') || '',
        'campaign_content': urlParams.get('utm_content') || '',
        'referrer': document.referrer || 'direct'
    };

    // Enhanced configuration for better data quality
    gtag('config', GA_ID, {
        // Fix referral issues - exclude your own domain
        'linker': {
            'domains': ['shopifyappauthority.com']
        },
        // Pass UTM data with page view
        'page_referrer': document.referrer,
        'campaign': {
            'source': utmData.campaign_source,
            'medium': utmData.campaign_medium,
            'name': utmData.campaign_name,
            'term': utmData.campaign_term,
            'content': utmData.campaign_content
        },
        // Enhanced measurement
        'send_page_view': true,
        // Custom dimensions
        'custom_map.dimension1': 'page_type',
        'custom_map.dimension2': 'merchant_name',
        'custom_map.dimension3': 'click_type',
        // Anonymize IP for GDPR compliance
        'anonymize_ip': true,
        // Debug mode
        'debug_mode': DEBUG_MODE
    });

    // Log referral source on page load
    if (document.referrer) {
        const referrerDomain = new URL(document.referrer).hostname.replace('www.', '');
        gtag('event', 'page_view_with_referrer', {
            'referrer_domain': referrerDomain,
            'referrer_url': document.referrer,
            'landing_page': window.location.pathname
        });
    }

    // Track Web Vitals for performance monitoring
    function trackWebVitals() {
        // Track Core Web Vitals
        if ('PerformanceObserver' in window) {
            // Largest Contentful Paint
            try {
                const po = new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        if (entry.entryType === 'largest-contentful-paint') {
                            gtag('event', 'LCP', {
                                'event_category': 'Web Vitals',
                                'event_label': 'Largest Contentful Paint',
                                'value': Math.round(entry.startTime),
                                'non_interaction': true
                            });
                        }
                    }
                });
                po.observe({type: 'largest-contentful-paint', buffered: true});
            } catch (e) {}

            // First Input Delay
            try {
                const po = new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        if (entry.entryType === 'first-input') {
                            gtag('event', 'FID', {
                                'event_category': 'Web Vitals',
                                'event_label': 'First Input Delay',
                                'value': Math.round(entry.processingStart - entry.startTime),
                                'non_interaction': true
                            });
                        }
                    }
                });
                po.observe({type: 'first-input', buffered: true});
            } catch (e) {}
        }
    }

    // Standardized event tracking
    window.trackEvent = function(eventName, parameters = {}) {
        if (DEBUG_MODE) {
            console.log('GA Event:', eventName, parameters);
        }
        gtag('event', eventName, parameters);
    };

    // SPECIFIC CLICK TRACKING YOU REQUESTED

    // 1. Track clicks to review sales pages (internal review links)
    function trackReviewPageClicks() {
        document.addEventListener('click', function(e) {
            const link = e.target.closest('a');
            if (link && link.hostname === window.location.hostname) {
                const href = link.pathname;

                // Check if it's a review page link
                if (href.includes('-review')) {
                    const reviewProduct = href.replace('/', '').replace('-review', '').replace('/', '');

                    gtag('event', 'review_page_click', {
                        'event_category': 'Navigation',
                        'event_label': reviewProduct,
                        'product_name': reviewProduct,
                        'from_page': window.location.pathname,
                        'to_page': href,
                        'link_text': link.textContent.trim(),
                        'link_position': getElementPosition(link)
                    });

                    if (DEBUG_MODE) {
                        console.log('Review Page Click:', reviewProduct);
                    }
                }
            }
        });
    }

    // 2. Track affiliate link clicks (external sponsored links)
    function trackAffiliateClicks() {
        document.addEventListener('click', function(e) {
            const link = e.target.closest('a[rel*="sponsored"], a[href*="shareasale"], a[href*="avantlink"], a[href*="partnerize"]');
            if (link && link.hostname !== window.location.hostname) {
                const merchant = getMerchantName(link);
                const linkType = link.rel?.includes('sponsored') ? 'sponsored' : 'affiliate';

                // Main affiliate click event
                gtag('event', 'affiliate_link_click', {
                    'event_category': 'Affiliate',
                    'event_label': merchant,
                    'merchant_name': merchant,
                    'destination_url': link.href,
                    'source_page': window.location.pathname,
                    'link_text': link.textContent.trim().substring(0, 100),
                    'link_type': linkType,
                    'link_position': getElementPosition(link)
                });

                // Also track which merchant specifically
                gtag('event', `affiliate_${merchant}_click`, {
                    'event_category': 'Affiliate_Merchant',
                    'event_label': link.textContent.trim(),
                    'destination_url': link.href,
                    'source_page': window.location.pathname
                });

                if (DEBUG_MODE) {
                    console.log('Affiliate Click:', merchant, link.href);
                }
            }
        });
    }

    // Helper function to extract merchant name from URL
    function getMerchantName(link) {
        const url = link.href.toLowerCase();
        const hostname = link.hostname.replace('www.', '');

        // Known merchant patterns
        const merchants = {
            'moosend.com': 'moosend',
            'activecampaign.com': 'activecampaign',
            'aweber.com': 'aweber',
            'mailchimp.com': 'mailchimp',
            'klaviyo.com': 'klaviyo',
            'getresponse.com': 'getresponse',
            'mailerlite.com': 'mailerlite',
            'constantcontact.com': 'constant_contact',
            'omnisend.com': 'omnisend',
            'drip.com': 'drip',
            'kit.com': 'kit',
            'convertkit.com': 'kit',
            'privy.com': 'privy',
            'justuno.com': 'justuno',
            'yotpo.com': 'yotpo',
            'stamped.io': 'stamped',
            'judge.me': 'judgeme',
            'okendo.io': 'okendo',
            'livechat.com': 'livechat',
            'gorgias.com': 'gorgias',
            'zendesk.com': 'zendesk',
            'hubspot.com': 'hubspot',
            'pipedrive.com': 'pipedrive',
            'close.com': 'close',
            'salesforce.com': 'salesforce',
            'triplewhale.com': 'triple_whale',
            'northbeam.io': 'northbeam',
            'hotjar.com': 'hotjar',
            'crazyegg.com': 'crazy_egg',
            'mixpanel.com': 'mixpanel',
            'kissmetrics.com': 'kissmetrics',
            'clickup.com': 'clickup',
            'monday.com': 'monday',
            'asana.com': 'asana',
            'trello.com': 'trello',
            'rebuyengine.com': 'rebuy',
            'rechargepayments.com': 'recharge',
            'postscript.io': 'postscript',
            'attentive.com': 'attentive',
            'leadpages.com': 'leadpages',
            'unbounce.com': 'unbounce',
            'instapage.com': 'instapage',
            'clickfunnels.com': 'clickfunnels',
            'builderall.com': 'builderall',
            'kartra.com': 'kartra',
            'sumo.com': 'sumo',
            'optinmonster.com': 'optinmonster',
            'thrivethemes.com': 'thrive'
        };

        // Check known merchants
        for (const [domain, name] of Object.entries(merchants)) {
            if (hostname.includes(domain) || url.includes(domain)) {
                return name;
            }
        }

        // Fallback to hostname
        return hostname.split('.')[0];
    }

    // Helper function to get element position on page
    function getElementPosition(element) {
        const allLinks = Array.from(document.querySelectorAll('a'));
        const position = allLinks.indexOf(element) + 1;
        const section = element.closest('section, article, header, footer, nav')?.className || 'unknown';
        return `${section}_position_${position}`;
    }

    // Track internal navigation patterns
    function trackInternalNavigation() {
        document.addEventListener('click', function(e) {
            const link = e.target.closest('a');
            if (link && link.hostname === window.location.hostname && !link.rel?.includes('sponsored')) {
                const fromPage = window.location.pathname;
                const toPage = link.pathname;

                // Only track significant navigation
                if (fromPage !== toPage) {
                    trackEvent('internal_navigation', {
                        'event_category': 'Navigation',
                        'from_page': fromPage,
                        'to_page': toPage,
                        'link_text': link.textContent.trim().substring(0, 50)
                    });
                }
            }
        });
    }

    // Track scroll depth
    function trackScrollDepth() {
        let maxScroll = 0;
        const thresholds = [25, 50, 75, 90, 100];
        let triggered = new Set();

        function checkScroll() {
            const scrollPercent = Math.round(
                (window.scrollY + window.innerHeight) / document.documentElement.scrollHeight * 100
            );

            if (scrollPercent > maxScroll) {
                maxScroll = scrollPercent;

                thresholds.forEach(threshold => {
                    if (scrollPercent >= threshold && !triggered.has(threshold)) {
                        triggered.add(threshold);
                        trackEvent('scroll_depth', {
                            'event_category': 'Engagement',
                            'event_label': `${threshold}%`,
                            'value': threshold,
                            'non_interaction': true
                        });
                    }
                });
            }
        }

        let scrollTimer;
        window.addEventListener('scroll', function() {
            clearTimeout(scrollTimer);
            scrollTimer = setTimeout(checkScroll, 100);
        });
    }

    // Track time on page
    function trackTimeOnPage() {
        const startTime = Date.now();
        const milestones = [30, 60, 120, 300]; // seconds
        let triggered = new Set();

        setInterval(function() {
            const timeOnPage = Math.round((Date.now() - startTime) / 1000);

            milestones.forEach(milestone => {
                if (timeOnPage >= milestone && !triggered.has(milestone)) {
                    triggered.add(milestone);
                    trackEvent('time_on_page', {
                        'event_category': 'Engagement',
                        'event_label': `${milestone} seconds`,
                        'value': milestone,
                        'non_interaction': true
                    });
                }
            });
        }, 5000);
    }

    // Track search usage
    function trackSearch() {
        // Track when search is opened
        document.addEventListener('click', function(e) {
            if (e.target.closest('.search-button, .search-icon, [aria-label*="Search"]')) {
                trackEvent('search_opened', {
                    'event_category': 'Site Search'
                });
            }
        });

        // Track search queries (if search box exists)
        const searchInputs = document.querySelectorAll('input[type="search"], input[name="q"], input[name="query"], #search-input');
        searchInputs.forEach(input => {
            let searchTimer;
            input.addEventListener('input', function() {
                clearTimeout(searchTimer);
                searchTimer = setTimeout(() => {
                    if (this.value.length > 2) {
                        trackEvent('search_query', {
                            'event_category': 'Site Search',
                            'search_term': this.value
                        });
                    }
                }, 1500);
            });
        });
    }

    // Track email capture interactions
    function trackEmailCapture() {
        // Track when popup shows
        window.addEventListener('email_popup_shown', function() {
            trackEvent('email_popup_displayed', {
                'event_category': 'Email Capture'
            });
        });

        // Track form submissions
        document.addEventListener('submit', function(e) {
            if (e.target.classList.contains('email-capture-form')) {
                const formType = e.target.dataset.captureType || 'unknown';
                trackEvent('email_signup', {
                    'event_category': 'Email Capture',
                    'event_label': formType,
                    'form_type': formType,
                    'page_location': window.location.pathname
                });
            }
        });
    }

    // Track page type for better content grouping
    function setPageType() {
        const path = window.location.pathname;
        let pageType = 'other';

        if (path === '/' || path === '/index.html') {
            pageType = 'homepage';
        } else if (path.includes('-review')) {
            pageType = 'review';
        } else if (path.includes('best-shopify-apps') || path.includes('best-email-marketing')) {
            pageType = 'listicle';
        } else if (path.startsWith('/blog/')) {
            pageType = 'blog';
        } else if (path.includes('methodology') || path.includes('privacy') || path.includes('terms') || path.includes('disclosure')) {
            pageType = 'legal';
        } else if (path.includes('faq')) {
            pageType = 'faq';
        }

        // Send page type as custom dimension
        gtag('event', 'page_view', {
            'page_type': pageType,
            'content_category': document.querySelector('meta[property="article:section"]')?.content || 'general'
        });

        return pageType;
    }

    // Initialize all tracking
    function initializeTracking() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
        } else {
            init();
        }

        function init() {
            // Set page type
            setPageType();

            // Initialize tracking features
            trackReviewPageClicks();  // Track clicks to review pages
            trackAffiliateClicks();    // Track affiliate link clicks
            trackInternalNavigation(); // Track other internal navigation
            trackScrollDepth();
            trackTimeOnPage();
            trackSearch();
            trackEmailCapture();
            trackWebVitals();

            if (DEBUG_MODE) {
                console.log('Google Analytics tracking initialized');
            }
        }
    }

    // Start tracking
    initializeTracking();

    // Expose tracking function globally
    window.GATracking = {
        trackEvent: trackEvent,
        debugMode: function(enable) {
            DEBUG_MODE = enable;
            console.log('GA Debug mode:', enable ? 'enabled' : 'disabled');
        }
    };

})();