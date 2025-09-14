// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    // Show/hide screenshot field based on payment type
    const paymentTypeRadios = document.querySelectorAll('input[name="paymentType"]');
    const screenshotField = document.getElementById('screenshotField');
    
    paymentTypeRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'online') {
                screenshotField.style.display = 'block';
                // Add animation
                screenshotField.style.animation = 'fadeIn 0.5s ease-out';
            } else {
                screenshotField.style.display = 'none';
            }
        });
    });
    
    // Set default date to today
    const dateField = document.getElementById('date');
    const today = new Date().toISOString().split('T')[0];
    dateField.value = today;
    
    // Form validation
    const paymentForm = document.getElementById('paymentForm');
    paymentForm.addEventListener('submit', function(e) {
        let valid = true;
        
        // Basic validation
        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const paymentType = document.querySelector('input[name="paymentType"]:checked').value;
        
        if (name === '') {
            alert('Please enter your name');
            valid = false;
        }
        
        if (email === '' || !email.includes('@')) {
            alert('Please enter a valid email address');
            valid = false;
        }
        
        if (paymentType === 'online') {
            const screenshot = document.getElementById('screenshot').value;
            if (screenshot === '') {
                alert('Please upload a screenshot for online payments');
                valid = false;
            }
        }
        
        if (!valid) {
            e.preventDefault();
        }
    });
    
    // Add animation to new table rows if any
    const tableRows = document.querySelectorAll('tbody tr');
    if (tableRows.length > 0) {
        tableRows[0].classList.add('new-row');
    }
});