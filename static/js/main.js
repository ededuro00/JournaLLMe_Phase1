/*
================================================================================
MAIN JAVASCRIPT FILE
================================================================================
This file contains interactive functionality for the questionnaire app.
Currently minimal - can be extended for additional features.
*/

// Run when the page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('Questionnaire App Loaded Successfully! 🎉');
    
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Auto-hide flash messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 300);
        }, 5000);
    });
});

// Add any additional JavaScript functionality here as needed
