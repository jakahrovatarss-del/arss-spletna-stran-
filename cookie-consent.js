// Google Consent Mode v2 Implementation
// Defines defaults, manages banner, and loads scripts upon consent.

(function () {
    // 1. Define dataLayer and the gtag function immediately
    window.dataLayer = window.dataLayer || [];
    function gtag() { dataLayer.push(arguments); }

    // 2. Set Default Consent State (Denied)
    // This blocks Analytics storage and ads until granted.
    gtag('consent', 'default', {
        'ad_storage': 'denied',
        'ad_user_data': 'denied',
        'ad_personalization': 'denied',
        'analytics_storage': 'denied',
        'wait_for_update': 500
    });

    // 3. Configuration
    const GA_ID = 'G-7EJYRWMP87';
    const CONSENT_KEY = 'arss_cookie_consent';

    // 4. Helper to load the Google Tag Script
    function loadGoogleTag() {
        // Correctly update consent to granted before loading script
        gtag('consent', 'update', {
            'ad_storage': 'granted',
            'ad_user_data': 'granted',
            'ad_personalization': 'granted',
            'analytics_storage': 'granted'
        });

        // Load the script if not already present
        if (!document.querySelector(`script[src*="${GA_ID}"]`)) {
            var script = document.createElement('script');
            script.async = true;
            script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_ID}`;
            document.head.appendChild(script);

            gtag('js', new Date());
            gtag('config', GA_ID);
            console.log('Google Analytics loaded (Consent Granted)');
        }
    }

    // 5. Check LocalStorage on page load
    const storedConsent = localStorage.getItem(CONSENT_KEY);

    if (storedConsent === 'granted') {
        // User previously granted consent -> Load immediately
        loadGoogleTag();
    } else if (storedConsent === 'denied') {
        // User previously denied -> Do nothing (defaults are already 'denied')
        console.log('Cookies denied by user preference.');
    } else {
        // No preference stored -> Show Banner
        window.addEventListener('DOMContentLoaded', showCookieBanner);
    }

    // 6. Create and Show Banner
    function showCookieBanner() {
        // Create banner element
        const banner = document.createElement('div');
        banner.id = 'cookie-consent-banner';
        banner.className = 'cookie-banner';

        banner.innerHTML = `
            <div class="cookie-content">
                <div class="cookie-text">
                    <h3>Ali dovolite piškotke?</h3>
                    <p>Za izboljšanje vaše uporabniške izkušnje in analizo prometa uporabljamo piškotke. 
                    Ali se strinjate z uporabo Google Analytics piškotkov?</p>
                </div>
                <div class="cookie-buttons">
                    <button id="btn-deny" class="cookie-btn-deny">Zavrni</button>
                    <button id="btn-accept" class="cookie-btn-accept">Dovoli</button>
                </div>
            </div>
        `;

        document.body.appendChild(banner);

        // Add Event Listeners
        document.getElementById('btn-accept').addEventListener('click', () => {
            localStorage.setItem(CONSENT_KEY, 'granted');
            loadGoogleTag();
            hideBanner();
        });

        document.getElementById('btn-deny').addEventListener('click', () => {
            localStorage.setItem(CONSENT_KEY, 'denied');
            hideBanner();
        });

        function hideBanner() {
            banner.classList.add('hide');
            setTimeout(() => {
                banner.remove();
            }, 500); // Wait for transition
        }

        // Slight delay for smooth entrance
        setTimeout(() => {
            banner.classList.add('show');
        }, 100);
    }

})();
