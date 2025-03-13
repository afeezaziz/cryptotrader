// Main JavaScript for Crypto Trader

document.addEventListener('DOMContentLoaded', function() {
    // Add loading indicator for form submissions
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                const originalText = submitButton.innerHTML;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
                submitButton.disabled = true;
                
                // Re-enable after 10 seconds in case of error
                setTimeout(() => {
                    submitButton.innerHTML = originalText;
                    submitButton.disabled = false;
                }, 10000);
            }
            
            // Add loading class to parent card if exists
            const card = this.closest('.card');
            if (card) {
                card.classList.add('loading');
                
                // Remove loading after 10 seconds in case of error
                setTimeout(() => {
                    card.classList.remove('loading');
                }, 10000);
            }
        });
    });
    
    // Auto-refresh orderbook data if on orderbook page
    const orderBookTables = document.querySelectorAll('.card-header h4');
    orderBookTables.forEach(header => {
        if (header.textContent.includes('Bids') || header.textContent.includes('Asks')) {
            // We're on the orderbook page
            const refreshInterval = 30000; // 30 seconds
            
            setInterval(() => {
                const currentUrl = window.location.href;
                if (currentUrl.includes('/orderbook')) {
                    // Only reload if we're still on the orderbook page
                    location.reload();
                }
            }, refreshInterval);
        }
    });
    
    // Add tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
