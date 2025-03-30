// Enable Bootstrap tooltips
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });

    return isValid;
}

// Dynamic team size fields
function toggleTeamSizeFields() {
    const isTeamEvent = document.getElementById('is_team_event');
    const teamSizeFields = document.getElementById('team_size_fields');
    
    if (isTeamEvent && teamSizeFields) {
        teamSizeFields.style.display = isTeamEvent.checked ? 'block' : 'none';
    }
}

// Initialize dynamic fields
document.addEventListener('DOMContentLoaded', function() {
    toggleTeamSizeFields();
});

// Add event listener to team event checkbox
const isTeamEvent = document.getElementById('is_team_event');
if (isTeamEvent) {
    isTeamEvent.addEventListener('change', toggleTeamSizeFields);
}

// Countdown timer for event registration
function updateCountdown(elementId, endDate) {
    const countdownElement = document.getElementById(elementId);
    if (!countdownElement) return;

    const end = new Date(endDate).getTime();

    const timer = setInterval(function() {
        const now = new Date().getTime();
        const distance = end - now;

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        countdownElement.innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;

        if (distance < 0) {
            clearInterval(timer);
            countdownElement.innerHTML = "Registration Closed";
        }
    }, 1000);
}

// Confirm delete actions
function confirmDelete(message = 'Are you sure you want to delete this item?') {
    return confirm(message);
}

// Handle file input preview
function handleImagePreview(input, previewId) {
    const preview = document.getElementById(previewId);
    if (!preview) return;

    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        }
        reader.readAsDataURL(input.files[0]);
    }
} 