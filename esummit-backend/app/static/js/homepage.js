// Homepage JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Testimonial Slider
    initTestimonialSlider();
    
    // Counter Animation
    initCounterAnimation();
    
    // Event Navigation
    initEventNavigation();
});

// Testimonial Slider
function initTestimonialSlider() {
    const testimonials = document.querySelectorAll('.testimonial-item');
    const indicators = document.querySelectorAll('.control-indicators .indicator');
    const prevBtn = document.querySelector('.control-prev');
    const nextBtn = document.querySelector('.control-next');
    
    if (!testimonials.length || !indicators.length) return;
    
    let currentIndex = 0;
    
    // Show testimonial at index
    function showTestimonial(index) {
        // Hide all testimonials
        testimonials.forEach(item => {
            item.classList.remove('active');
        });
        
        // Remove active class from all indicators
        indicators.forEach(indicator => {
            indicator.classList.remove('active');
        });
        
        // Show current testimonial and activate indicator
        testimonials[index].classList.add('active');
        indicators[index].classList.add('active');
        
        currentIndex = index;
    }
    
    // Next testimonial
    function nextTestimonial() {
        let nextIndex = currentIndex + 1;
        if (nextIndex >= testimonials.length) {
            nextIndex = 0;
        }
        showTestimonial(nextIndex);
    }
    
    // Previous testimonial
    function prevTestimonial() {
        let prevIndex = currentIndex - 1;
        if (prevIndex < 0) {
            prevIndex = testimonials.length - 1;
        }
        showTestimonial(prevIndex);
    }
    
    // Add click event to indicators
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => {
            showTestimonial(index);
        });
    });
    
    // Add click event to prev/next buttons
    if (prevBtn) prevBtn.addEventListener('click', prevTestimonial);
    if (nextBtn) nextBtn.addEventListener('click', nextTestimonial);
    
    // Auto rotate testimonials
    setInterval(nextTestimonial, 5000);
}

// Counter Animation
function initCounterAnimation() {
    const counters = document.querySelectorAll('.counter');
    
    if (!counters.length) return;
    
    const speed = 200;
    
    const animateCounter = (counter) => {
        const target = +counter.innerText;
        const count = 0;
        const increment = target / speed;
        
        const updateCount = () => {
            const value = Math.ceil(count);
            counter.innerText = value;
            
            if (value < target) {
                count += increment;
                setTimeout(updateCount, 1);
            } else {
                counter.innerText = target;
            }
        };
        
        updateCount();
    };
    
    // Use Intersection Observer to trigger counter animation when visible
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    counters.forEach(counter => {
        observer.observe(counter);
    });
}

// Event Navigation
function initEventNavigation() {
    const prevBtn = document.querySelector('.events-navigation .nav-prev');
    const nextBtn = document.querySelector('.events-navigation .nav-next');
    const eventsRow = document.querySelector('.events-slider .row');
    
    if (!prevBtn || !nextBtn || !eventsRow) return;
    
    // Simple navigation for demo purposes
    // In a real implementation, this would be a proper carousel
    prevBtn.addEventListener('click', () => {
        eventsRow.style.transform = 'translateX(0)';
    });
    
    nextBtn.addEventListener('click', () => {
        eventsRow.style.transform = 'translateX(-10px)';
        setTimeout(() => {
            eventsRow.style.transform = 'translateX(0)';
        }, 300);
    });
}
