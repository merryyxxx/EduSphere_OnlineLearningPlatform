/**
 * EduSphere - Main JavaScript File
 * Modern warm theme interactions and enhancements
 */

// Document Ready
$(document).ready(function() {
    console.log('🎓 EduSphere Platform Initialized');
    
    // Initialize features
    initializeTooltips();
    autoHideAlerts();
    setupSmoothScroll();
    setupFormValidations();
    addAnimations();
    
    // Initialize active nav states
    highlightActiveNav();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Auto-hide alert messages after 5 seconds
 */
function autoHideAlerts() {
    $('.alert').not('.alert-permanent').each(function() {
        const alert = $(this);
        setTimeout(function() {
            alert.fadeOut('slow', function() {
                $(this).remove();
            });
        }, 5000);
    });
}

/**
 * Setup smooth scrolling for anchor links
 */
function setupSmoothScroll() {
    $('a[href*="#"]:not([href="#"])').click(function(e) {
        if (location.pathname.replace(/^\//, '') === this.pathname.replace(/^\//, '') 
            && location.hostname === this.hostname) {
            let target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                e.preventDefault();
                $('html, body').animate({
                    scrollTop: target.offset().top - 80
                }, 800, 'swing');
            }
        }
    });
}

/**
 * Highlight active navigation item
 */
function highlightActiveNav() {
    const currentPath = window.location.pathname;
    $('.nav-link').each(function() {
        const href = $(this).attr('href');
        if (href === currentPath || (currentPath.includes(href) && href !== '/')) {
            $(this).addClass('active');
        }
    });
}

/**
 * Add scroll animations
 */
function addAnimations() {
    // Fade in elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe cards
    document.querySelectorAll('.card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
}

/**
 * Form Validation Setup
 */
function setupFormValidations() {
    // Email validation
    $('input[type="email"]').on('blur', function() {
        validateEmail($(this));
    });
    
    // Password strength indicator
    $('input[type="password"]').on('input', function() {
        if ($(this).attr('id') === 'password') {
            showPasswordStrength($(this));
        }
    });
    
    // Number inputs validation
    $('input[type="number"]').on('input', function() {
        const val = parseFloat($(this).val());
        const min = parseFloat($(this).attr('min'));
        const max = parseFloat($(this).attr('max'));
        
        if (min !== undefined && val < min) {
            $(this).val(min);
        }
        if (max !== undefined && val > max) {
            $(this).val(max);
        }
    });
}

/**
 * Validate email format
 */
function validateEmail(input) {
    const email = input.val();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (email && !emailRegex.test(email)) {
        input.addClass('is-invalid');
        if (!input.next('.invalid-feedback').length) {
            input.after('<div class="invalid-feedback">Please enter a valid email address</div>');
        }
    } else {
        input.removeClass('is-invalid');
        input.next('.invalid-feedback').remove();
    }
}

/**
 * Show password strength indicator
 */
function showPasswordStrength(input) {
    const password = input.val();
    let strength = 0;
    let strengthText = '';
    let strengthClass = '';
    
    if (password.length >= 6) strength++;
    if (password.length >= 10) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[^a-zA-Z\d]/.test(password)) strength++;
    
    switch(strength) {
        case 0:
        case 1:
            strengthText = 'Weak';
            strengthClass = 'text-danger';
            break;
        case 2:
        case 3:
            strengthText = 'Medium';
            strengthClass = 'text-warning';
            break;
        case 4:
        case 5:
            strengthText = 'Strong';
            strengthClass = 'text-success';
            break;
    }
    
    // Remove existing indicator
    input.siblings('.password-strength').remove();
    
    // Add new indicator
    if (password.length > 0) {
        input.after(`<small class="password-strength ${strengthClass} d-block mt-1">
            <i class="bi bi-shield-fill"></i> Password strength: ${strengthText}
        </small>`);
    }
}

/**
 * Show Loading Spinner on Buttons
 */
function showButtonLoading(button) {
    const $btn = $(button);
    $btn.data('original-html', $btn.html());
    $btn.html('<span class="spinner-border spinner-border-sm me-2"></span>Loading...');
    $btn.prop('disabled', true);
}

function hideButtonLoading(button) {
    const $btn = $(button);
    $btn.html($btn.data('original-html'));
    $btn.prop('disabled', false);
}

/**
 * Format Currency
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

/**
 * Format Date
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

/**
 * Show Toast Notification (Custom for warm theme)
 */
function showToast(message, type = 'info') {
    const bgColors = {
        'success': 'var(--accent-green)',
        'error': 'var(--accent-orange)',
        'warning': 'var(--accent-yellow)',
        'info': 'var(--accent-blue)'
    };
    
    const icons = {
        'success': 'bi-check-circle-fill',
        'error': 'bi-exclamation-triangle-fill',
        'warning': 'bi-exclamation-circle-fill',
        'info': 'bi-info-circle-fill'
    };
    
    const toast = $(`
        <div class="toast-custom" style="
            position: fixed;
            top: 100px;
            right: 20px;
            background: white;
            border: 2px solid var(--border-color);
            border-left: 4px solid ${bgColors[type]};
            border-radius: var(--border-radius-sm);
            padding: 1rem 1.5rem;
            box-shadow: var(--box-shadow-hover);
            z-index: 9999;
            max-width: 400px;
            animation: slideInRight 0.3s ease;
        ">
            <div class="d-flex align-items-center">
                <i class="bi ${icons[type]} me-3" style="font-size: 1.5rem; color: ${bgColors[type]};"></i>
                <div class="flex-grow-1">${message}</div>
                <button type="button" class="btn-close ms-3" onclick="this.parentElement.parentElement.remove()"></button>
            </div>
        </div>
    `);
    
    $('body').append(toast);
    
    setTimeout(function() {
        toast.fadeOut(300, function() {
            $(this).remove();
        });
    }, 5000);
}

/**
 * Confirm Dialog (Custom styled)
 */
function confirmAction(message, callback) {
    if (confirm(message)) {
        if (typeof callback === 'function') {
            callback();
        }
        return true;
    }
    return false;
}

/**
 * Back to Top Button
 */
$(window).scroll(function() {
    if ($(this).scrollTop() > 400) {
        if (!$('.back-to-top').length) {
            $('body').append(`
                <button class="back-to-top btn btn-primary" 
                        style="position: fixed; bottom: 30px; right: 30px; z-index: 999; 
                               border-radius: 50%; width: 50px; height: 50px; 
                               box-shadow: var(--box-shadow-hover);">
                    <i class="bi bi-arrow-up" style="font-size: 1.2rem;"></i>
                </button>
            `);
        }
        $('.back-to-top').fadeIn();
    } else {
        $('.back-to-top').fadeOut();
    }
});

$(document).on('click', '.back-to-top', function() {
    $('html, body').animate({ scrollTop: 0 }, 600);
});

/**
 * Prevent double form submission
 */
$('form').on('submit', function(e) {
    const $form = $(this);
    const $submitBtn = $form.find('button[type="submit"], input[type="submit"]');
    
    if ($form.data('submitted') === true) {
        e.preventDefault();
        return false;
    }
    
    $form.data('submitted', true);
    $submitBtn.prop('disabled', true);
    
    setTimeout(function() {
        $form.data('submitted', false);
        $submitBtn.prop('disabled', false);
    }, 3000);
});

/**
 * Search Enhancement with Debounce
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Live search functionality
const searchInput = document.querySelector('input[name="search"]');
if (searchInput) {
    const handleSearch = debounce(function(e) {
        const searchTerm = e.target.value;
        if (searchTerm.length >= 3) {
            console.log('Searching for:', searchTerm);
            // Can implement AJAX search here
        }
    }, 500);
    
    searchInput.addEventListener('input', handleSearch);
}

/**
 * Card Hover Effects
 */
$('.course-card, .category-card').hover(
    function() {
        $(this).css('transform', 'translateY(-8px)');
    },
    function() {
        $(this).css('transform', 'translateY(0)');
    }
);

/**
 * Tab State Persistence
 */
$('button[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {
    const tabId = $(e.target).attr('data-bs-target');
    localStorage.setItem('activeTab', tabId);
});

// Restore active tab
$(document).ready(function() {
    const activeTab = localStorage.getItem('activeTab');
    if (activeTab) {
        $(`button[data-bs-target="${activeTab}"]`).tab('show');
    }
});

/**
 * Navbar Scroll Effect
 */
$(window).scroll(function() {
    if ($(this).scrollTop() > 50) {
        $('.navbar').addClass('scrolled');
    } else {
        $('.navbar').removeClass('scrolled');
    }
});

/**
 * Export functions for use in templates
 */
window.EduSphere = {
    showToast,
    formatCurrency,
    formatDate,
    confirmAction,
    showButtonLoading,
    hideButtonLoading,
    debounce
};

console.log('✨ EduSphere JavaScript Ready!');