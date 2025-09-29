// Email Capture System with GDPR Compliance
class EmailCapture {
    constructor() {
        this.consentGiven = false;
        this.googleSheetURL = 'YOUR_GOOGLE_APPS_SCRIPT_URL'; // We'll set this up
        this.init();
    }

    init() {
        // Initialize all email forms on the page
        this.initializeForms();

        // Initialize popup if enabled
        if (this.shouldShowPopup()) {
            this.initializePopup();
        }
    }

    initializeForms() {
        const forms = document.querySelectorAll('.email-capture-form, form[data-email-capture]');
        forms.forEach(form => this.setupForm(form));
    }

    setupForm(form) {
        // Add GDPR compliance fields if not present
        if (!form.querySelector('.gdpr-consent')) {
            const consentHTML = `
                <div class="gdpr-consent" style="margin: 15px 0; font-size: 14px;">
                    <label style="display: flex; align-items: flex-start; cursor: pointer;">
                        <input type="checkbox" name="gdpr_consent" required style="margin-right: 8px; margin-top: 3px;">
                        <span>I agree to receive emails and accept the <a href="/privacy-policy/" target="_blank" style="color: #95bf47;">Privacy Policy</a>. You can unsubscribe at any time.</span>
                    </label>
                </div>
            `;

            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.insertAdjacentHTML('beforebegin', consentHTML);
            }
        }

        // Handle form submission
        form.addEventListener('submit', (e) => this.handleSubmit(e, form));
    }

    async handleSubmit(e, form) {
        e.preventDefault();

        const formData = new FormData(form);
        const email = formData.get('email');
        const consent = formData.get('gdpr_consent');

        if (!consent) {
            alert('Please accept the privacy policy to continue.');
            return;
        }

        // Get UTM parameters from URL
        const urlParams = new URLSearchParams(window.location.search);

        // Prepare data for submission
        const data = {
            email: email,
            consent: true,
            timestamp: new Date().toISOString(),
            source: window.location.pathname,
            type: form.dataset.captureType || 'newsletter',
            referrer: document.referrer,
            userAgent: navigator.userAgent,
            utm_source: urlParams.get('utm_source') || '',
            utm_medium: urlParams.get('utm_medium') || '',
            utm_campaign: urlParams.get('utm_campaign') || ''
        };

        try {
            // Send to Google Sheets
            await this.sendToGoogleSheets(data);

            // Show success message
            this.showSuccess(form);

            // Set cookie to prevent popup from showing again
            this.setEmailCapturedCookie();

            // Close popup if it's the popup form
            if (form.closest('.email-popup')) {
                this.closePopup();
            }

        } catch (error) {
            console.error('Error submitting email:', error);
            alert('There was an error. Please try again.');
        }
    }

    async sendToGoogleSheets(data) {
        // Google Apps Script endpoint (we'll create this)
        const response = await fetch(this.googleSheetURL, {
            method: 'POST',
            mode: 'no-cors',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        // Note: no-cors mode doesn't allow reading response
        // We assume success if no error is thrown
        return true;
    }

    showSuccess(form) {
        const successMessage = document.createElement('div');
        successMessage.className = 'email-success';
        successMessage.style.cssText = `
            background: #95bf47;
            color: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            margin-top: 10px;
        `;
        successMessage.textContent = 'Thank you for subscribing! Check your email for confirmation.';

        form.style.display = 'none';
        form.parentNode.insertBefore(successMessage, form.nextSibling);
    }

    // Popup functionality
    initializePopup() {
        // Wait before showing popup (e.g., 30 seconds or on exit intent)
        setTimeout(() => this.showPopup(), 30000);

        // Exit intent detection
        document.addEventListener('mouseout', (e) => {
            if (e.clientY <= 0 && !this.popupShown && this.shouldShowPopup()) {
                this.showPopup();
            }
        });
    }

    shouldShowPopup() {
        // Check if user has already subscribed or dismissed popup
        const emailCaptured = this.getCookie('email_captured');
        const popupDismissed = this.getCookie('popup_dismissed');
        const lastShown = this.getCookie('popup_last_shown');

        if (emailCaptured || popupDismissed) return false;

        // Don't show more than once per day
        if (lastShown) {
            const dayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);
            if (new Date(lastShown) > dayAgo) return false;
        }

        return true;
    }

    showPopup() {
        if (this.popupShown || !this.shouldShowPopup()) return;

        this.popupShown = true;
        this.setCookie('popup_last_shown', new Date().toISOString(), 1);

        const popupHTML = `
            <div class="email-popup-overlay" style="
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.5);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
                animation: fadeIn 0.3s ease;
            ">
                <div class="email-popup" style="
                    background: white;
                    padding: 40px;
                    border-radius: 12px;
                    max-width: 500px;
                    width: 90%;
                    position: relative;
                    animation: slideUp 0.3s ease;
                    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
                ">
                    <button class="popup-close" style="
                        position: absolute;
                        top: 15px;
                        right: 15px;
                        background: none;
                        border: none;
                        font-size: 30px;
                        cursor: pointer;
                        color: #718096;
                        line-height: 1;
                        padding: 0;
                        width: 30px;
                        height: 30px;
                    ">&times;</button>

                    <h2 style="
                        color: #1a202c;
                        margin-bottom: 15px;
                        font-size: 28px;
                        font-weight: 700;
                    ">Get 10% More Sales with the Right Apps</h2>

                    <p style="
                        color: #4a5568;
                        margin-bottom: 25px;
                        font-size: 16px;
                        line-height: 1.6;
                    ">Join 5,000+ store owners getting exclusive app recommendations and growth strategies.</p>

                    <form class="email-capture-form" data-capture-type="popup" style="margin: 0;">
                        <input type="email" name="email" placeholder="Enter your email" required style="
                            width: 100%;
                            padding: 15px;
                            border: 2px solid #e2e8f0;
                            border-radius: 8px;
                            font-size: 16px;
                            margin-bottom: 15px;
                            box-sizing: border-box;
                        ">

                        <div class="gdpr-consent" style="margin: 15px 0; font-size: 14px;">
                            <label style="display: flex; align-items: flex-start; cursor: pointer;">
                                <input type="checkbox" name="gdpr_consent" required style="margin-right: 8px; margin-top: 3px;">
                                <span>I agree to receive emails and accept the <a href="/privacy-policy/" target="_blank" style="color: #95bf47;">Privacy Policy</a>.</span>
                            </label>
                        </div>

                        <button type="submit" style="
                            width: 100%;
                            background: linear-gradient(135deg, #95bf47 0%, #7fa83a 100%);
                            color: white;
                            padding: 15px;
                            border: none;
                            border-radius: 8px;
                            font-size: 18px;
                            font-weight: 700;
                            cursor: pointer;
                            transition: transform 0.2s;
                        ">Get Free Recommendations</button>
                    </form>

                    <p style="
                        text-align: center;
                        color: #a0aec0;
                        font-size: 12px;
                        margin-top: 15px;
                        margin-bottom: 0;
                    ">No spam. Unsubscribe anytime.</p>
                </div>
            </div>

            <style>
                @keyframes fadeIn {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }
                @keyframes slideUp {
                    from { transform: translateY(20px); opacity: 0; }
                    to { transform: translateY(0); opacity: 1; }
                }
                .email-popup button[type="submit"]:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(149, 191, 71, 0.4);
                }
            </style>
        `;

        const popupContainer = document.createElement('div');
        popupContainer.innerHTML = popupHTML;
        document.body.appendChild(popupContainer.firstElementChild);

        // Setup popup form
        const popupForm = document.querySelector('.email-popup form');
        this.setupForm(popupForm);

        // Close button functionality
        document.querySelector('.popup-close').addEventListener('click', () => {
            this.closePopup();
            this.setCookie('popup_dismissed', 'true', 7);
        });

        // Close on overlay click
        document.querySelector('.email-popup-overlay').addEventListener('click', (e) => {
            if (e.target === e.currentTarget) {
                this.closePopup();
                this.setCookie('popup_dismissed', 'true', 7);
            }
        });
    }

    closePopup() {
        const popup = document.querySelector('.email-popup-overlay');
        if (popup) {
            popup.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => popup.remove(), 300);
        }
    }

    // Cookie utilities
    setCookie(name, value, days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = "expires=" + date.toUTCString();
        document.cookie = name + "=" + value + ";" + expires + ";path=/";
    }

    getCookie(name) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for(let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) == ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }

    setEmailCapturedCookie() {
        this.setCookie('email_captured', 'true', 365);
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new EmailCapture());
} else {
    new EmailCapture();
}

// Add fadeOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
`;
document.head.appendChild(style);