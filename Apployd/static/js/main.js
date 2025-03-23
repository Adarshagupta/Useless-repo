// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Flask application loaded');
    
    // Add a simple animation to the heading
    const heading = document.querySelector('h1');
    if (heading) {
        heading.style.opacity = '0';
        setTimeout(() => {
            heading.style.transition = 'opacity 1s ease-in-out';
            heading.style.opacity = '1';
        }, 300);
    }
}); 