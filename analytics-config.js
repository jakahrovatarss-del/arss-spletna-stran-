// Google Analytics Configuration
// Replace 'GA_MEASUREMENT_ID' with your actual Google Analytics Measurement ID
const GA_MEASUREMENT_ID = 'GA_MEASUREMENT_ID'; // Format: G-XXXXXXXXXX

// Initialize Google Analytics
window.dataLayer = window.dataLayer || [];
function gtag() { dataLayer.push(arguments); }
gtag('js', new Date());
gtag('config', GA_MEASUREMENT_ID, {
    'anonymize_ip': true, // GDPR compliance
    'cookie_flags': 'SameSite=None;Secure'
});

// Track custom events (optional)
function trackEvent(eventName, eventParams = {}) {
    gtag('event', eventName, eventParams);
}

// Track page views (for single-page apps)
function trackPageView(pagePath) {
    gtag('config', GA_MEASUREMENT_ID, {
        'page_path': pagePath
    });
}

// Export functions for use in other scripts
window.trackEvent = trackEvent;
window.trackPageView = trackPageView;
