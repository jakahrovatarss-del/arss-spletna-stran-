// Formspree Configuration
// Replace 'FORMSPREE_ENDPOINT' with your actual Formspree form endpoint
const FORMSPREE_ENDPOINT = 'https://formspree.io/f/mgvgnnjl'; // Updated with correct ID

// Handle form submission
document.addEventListener('DOMContentLoaded', () => {
    const contactForm = document.querySelector('.contact-form');

    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const submitButton = contactForm.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.textContent;

            // Disable button and show loading state
            submitButton.disabled = true;
            submitButton.textContent = 'Pošiljam...';

            try {
                const formData = new FormData(contactForm);

                const response = await fetch(FORMSPREE_ENDPOINT, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Accept': 'application/json'
                    }
                });

                if (response.ok) {
                    // Success
                    showMessage('success', '✅ Hvala! Vaše sporočilo je bilo uspešno poslano. Kontaktirali vas bomo v najkrajšem možnem času.');
                    contactForm.reset();

                    // Track form submission in Google Analytics
                    if (typeof trackEvent !== 'undefined') {
                        trackEvent('form_submission', {
                            'form_name': 'contact_form',
                            'form_location': window.location.pathname
                        });
                    }
                } else {
                    // Error from Formspree
                    const data = await response.json();
                    throw new Error(data.error || 'Napaka pri pošiljanju');
                }
            } catch (error) {
                // Network or other error
                console.error('Form submission error:', error);
                showMessage('error', '❌ Oprostite, prišlo je do napake. Prosimo, poskusite znova ali nas kontaktirajte direktno na info@arss.si');
            } finally {
                // Re-enable button
                submitButton.disabled = false;
                submitButton.textContent = originalButtonText;
            }
        });
    }
});

// Show success/error message
function showMessage(type, message) {
    // Remove any existing messages
    const existingMessage = document.querySelector('.form-message');
    if (existingMessage) {
        existingMessage.remove();
    }

    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.className = `form-message form-message-${type}`;
    messageDiv.textContent = message;

    // Insert message before form
    const contactForm = document.querySelector('.contact-form');
    contactForm.parentNode.insertBefore(messageDiv, contactForm);

    // Auto-remove message after 10 seconds
    setTimeout(() => {
        messageDiv.style.opacity = '0';
        setTimeout(() => messageDiv.remove(), 300);
    }, 10000);
}
