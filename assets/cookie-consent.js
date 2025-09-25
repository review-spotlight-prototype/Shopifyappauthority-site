/**
 * Global Cookie Consent System
 * GDPR compliant cookie consent banner
 */

(function() {
    'use strict';

    const COOKIE_NAME = 'cookie-consent';
    const COOKIE_DURATION = 365; // days

    // Cookie utility functions
    function setCookie(name, value, days) {
        const expires = new Date();
        expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
        document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/;SameSite=Lax`;
    }

    function getCookie(name) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for(let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }

    function hasConsented() {
        return getCookie(COOKIE_NAME) !== null;
    }

    function createConsentBanner() {
        const banner = document.createElement('div');
        banner.className = 'cookie-consent-banner';
        banner.id = 'cookieConsentBanner';

        banner.innerHTML = `
            <div class="cookie-consent-content">
                <div class="cookie-consent-text">
                    <p>We use cookies to enhance your browsing experience, analyze site traffic, and personalize content. By continuing to use this site, you consent to our use of cookies. <a href="/privacy-policy" target="_blank">Learn more</a></p>
                </div>
                <div class="cookie-consent-buttons">
                    <button class="cookie-consent-btn accept" id="acceptCookies">Accept All</button>
                    <button class="cookie-consent-btn reject" id="rejectCookies">Decline</button>
                </div>
            </div>
        `;

        return banner;
    }

    function showBanner() {
        if (document.getElementById('cookieConsentBanner')) {
            return; // Banner already exists
        }

        const banner = createConsentBanner();
        document.body.appendChild(banner);

        // Add event listeners
        const acceptBtn = document.getElementById('acceptCookies');
        const rejectBtn = document.getElementById('rejectCookies');

        if (acceptBtn) {
            acceptBtn.addEventListener('click', acceptCookies);
        }

        if (rejectBtn) {
            rejectBtn.addEventListener('click', rejectCookies);
        }

        // Animate in
        setTimeout(() => {
            banner.style.transform = 'translateY(0)';
        }, 100);
    }

    function hideBanner() {
        const banner = document.getElementById('cookieConsentBanner');
        if (banner) {
            banner.classList.add('hidden');
            setTimeout(() => {
                if (banner.parentNode) {
                    banner.parentNode.removeChild(banner);
                }
            }, 300);
        }
    }

    function acceptCookies() {
        setCookie(COOKIE_NAME, 'accepted', COOKIE_DURATION);
        hideBanner();

        // Trigger accepted event for analytics/other scripts
        if (typeof window.cookieConsentAccepted === 'function') {
            window.cookieConsentAccepted();
        }

        // Dispatch custom event
        window.dispatchEvent(new CustomEvent('cookieConsentAccepted', {
            detail: { consent: 'accepted' }
        }));
    }

    function rejectCookies() {
        setCookie(COOKIE_NAME, 'rejected', COOKIE_DURATION);
        hideBanner();

        // Clear existing cookies (except essential ones)
        const cookies = document.cookie.split(';');
        cookies.forEach(cookie => {
            const eqPos = cookie.indexOf('=');
            const name = eqPos > -1 ? cookie.substr(0, eqPos).trim() : cookie.trim();

            // Don't delete essential cookies
            if (name !== COOKIE_NAME && name !== 'session' && name !== 'csrf_token') {
                document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/`;
                document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain=${window.location.hostname}`;
            }
        });

        // Trigger rejected event
        if (typeof window.cookieConsentRejected === 'function') {
            window.cookieConsentRejected();
        }

        // Dispatch custom event
        window.dispatchEvent(new CustomEvent('cookieConsentRejected', {
            detail: { consent: 'rejected' }
        }));
    }

    function init() {
        // Only show banner if consent hasn't been given
        if (!hasConsented()) {
            showBanner();
        }
    }

    // Public API
    window.CookieConsent = {
        init: init,
        show: showBanner,
        hide: hideBanner,
        accept: acceptCookies,
        reject: rejectCookies,
        hasConsented: hasConsented,
        getConsent: () => getCookie(COOKIE_NAME)
    };

    // Auto-initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();