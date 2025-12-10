// Form Enhancement Script
// Handles: File upload feedback only (submission is native to Formsubmit.co)

document.addEventListener('DOMContentLoaded', () => {
    // File Upload Feedback Logic (only for Gospodinjstva page)
    const fileInput = document.getElementById('meter-image');
    if (fileInput) {
        const fileLabel = document.querySelector('label[for="meter-image"]');
        if (fileLabel) {
            const originalLabelText = fileLabel.textContent;

            fileInput.addEventListener('change', (e) => {
                if (e.target.files && e.target.files.length > 0) {
                    // Sanitize filename to prevent XSS
                    const fileName = e.target.files[0].name.replace(/</g, '&lt;').replace(/>/g, '&gt;');
                    fileLabel.textContent = `✅ Datoteka izbrana: ${fileName}`;
                    fileLabel.style.color = '#10b981';
                } else {
                    fileLabel.textContent = originalLabelText;
                    fileLabel.style.color = '';
                }
            });
        }
    }

    // Submit button loading state (optional enhancement)
    const allForms = document.querySelectorAll('.contact-form');
    allForms.forEach(form => {
        form.addEventListener('submit', function () {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Pošiljam...';
            }
            // Form submits naturally - no preventDefault
        });
    });
});
