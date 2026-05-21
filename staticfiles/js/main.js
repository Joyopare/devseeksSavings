// Main JavaScript file for Finance Savings App

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initializeTheme();
    initializeToasts();
    initializeTableFilters();
    initializeBackToTop();
    initializeFormValidation();
    initializeAnimations();
    initializeTooltips();
    initializeProgressBars();
});

function initializeTheme() {
    const btn = document.getElementById('themeToggle');
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const stored = localStorage.getItem('theme');
    const effective = stored || (prefersDark ? 'dark' : 'light');

    setTheme(effective);

    if (btn) {
        btn.addEventListener('click', () => {
            const next = document.body.classList.contains('dark-mode') ? 'light' : 'dark';
            setTheme(next);
            localStorage.setItem('theme', next);
        });
    }
}

function setTheme(theme) {
    const isDark = theme === 'dark';
    document.body.classList.toggle('dark-mode', isDark);
    const btn = document.getElementById('themeToggle');
    if (btn) {
        const icon = btn.querySelector('i');
        if (icon) icon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
        btn.title = isDark ? 'Switch to light mode' : 'Switch to dark mode';
    }
}

function initializeToasts() {
    if (typeof bootstrap === 'undefined' || !bootstrap.Toast) return;
    document.querySelectorAll('.toast').forEach((el) => {
        try {
            const toast = new bootstrap.Toast(el);
            toast.show();
        } catch (e) {
            // ignore
        }
    });
}

function initializeTableFilters() {
    document.querySelectorAll('[data-table-filter]').forEach((input) => {
        const tableId = input.getAttribute('data-table-filter');
        const table = document.getElementById(tableId);
        if (!table) return;

        input.addEventListener('input', () => {
            const q = (input.value || '').toLowerCase();
            table.querySelectorAll('tbody tr').forEach((tr) => {
                const text = (tr.textContent || '').toLowerCase();
                tr.style.display = text.includes(q) ? '' : 'none';
            });
        });
    });
}

function initializeBackToTop() {
    const btn = document.getElementById('backToTop');
    if (!btn) return;

    const onScroll = () => {
        btn.classList.toggle('show', window.scrollY > 600);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    btn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// Form validation enhancement
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                // Add loading state
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner"></span> Processing...';
                submitBtn.disabled = true;
                
                // NOTE: We don't auto-reset here; server navigation/response should restore state.
                // Keeping it disabled prevents accidental double-submits.
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid')) {
                    validateField(this);
                }
            });
        });
    });
}

// Field validation
function validateField(field) {
    const value = field.value.trim();
    const fieldType = field.type;
    let isValid = true;
    let errorMessage = '';
    
    // Remove existing validation classes
    field.classList.remove('is-invalid', 'is-valid');
    
    // Required field validation
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        errorMessage = 'This field is required.';
    }
    
    // Number validation
    if (fieldType === 'number' && value) {
        const numValue = parseFloat(value);
        const min = parseFloat(field.getAttribute('min'));
        const max = parseFloat(field.getAttribute('max'));
        
        if (isNaN(numValue)) {
            isValid = false;
            errorMessage = 'Please enter a valid number.';
        } else if (min !== null && numValue < min) {
            isValid = false;
            errorMessage = `Minimum value is ${min}.`;
        } else if (max !== null && numValue > max) {
            isValid = false;
            errorMessage = `Maximum value is ${max}.`;
        }
    }
    
    // Email validation
    if (fieldType === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid email address.';
        }
    }
    
    // Apply validation styling
    if (!isValid) {
        field.classList.add('is-invalid');
        showFieldError(field, errorMessage);
    } else {
        field.classList.add('is-valid');
        hideFieldError(field);
    }
    
    return isValid;
}

// Show field error message
function showFieldError(field, message) {
    hideFieldError(field); // Remove existing error
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
}

// Hide field error message
function hideFieldError(field) {
    const existingError = field.parentNode.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }
}

// Initialize animations
function initializeAnimations() {
    // Animate balance displays on page load
    const balanceDisplays = document.querySelectorAll('.balance-display');
    balanceDisplays.forEach(display => {
        animateValue(display, 0, parseFloat(display.textContent.replace('GH₵', '').replace(',', '')), 1000);
    });
    
    // Animate progress bars
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
        }, 100);
    });
}

// Animate numeric values
function animateValue(element, start, end, duration) {
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const currentValue = start + (end - start) * progress;
        element.textContent = 'GH₵' + currentValue.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize progress bars with additional functionality
function initializeProgressBars() {
    const progressBars = document.querySelectorAll('.progress');
    
    progressBars.forEach(progressBar => {
        const bar = progressBar.querySelector('.progress-bar');
        if (bar) {
            const percentage = parseFloat(bar.style.width);
            
            // Add color based on percentage
            if (percentage >= 100) {
                bar.classList.add('bg-success');
            } else if (percentage >= 75) {
                bar.classList.add('bg-info');
            } else if (percentage >= 50) {
                bar.classList.add('bg-warning');
            } else {
                bar.classList.add('bg-danger');
            }
            
            // Add hover effect
            progressBar.addEventListener('mouseenter', function() {
                bar.style.transform = 'scaleY(1.2)';
            });
            
            progressBar.addEventListener('mouseleave', function() {
                bar.style.transform = 'scaleY(1)';
            });
        }
    });
}

// Utility function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Utility function to show confirmation dialog - REMOVED for one-click approval
// function confirmAction(message, callback) {
//     if (confirm(message)) {
//         callback();
//     }
// }

// Auto-refresh functionality (for dashboard)
function initializeAutoRefresh(interval = 30000) {
    const dashboardPages = ['dashboard', 'savings_overview'];
    const currentPath = window.location.pathname;
    
    if (dashboardPages.some(page => currentPath.includes(page))) {
        setInterval(() => {
            // Only refresh if user is active
            if (document.hasFocus()) {
                location.reload();
            }
        }, interval);
    }
}

// Print functionality
function printTransactionHistory() {
    window.print();
}

// Export functionality (placeholder for future implementation)
function exportTransactionHistory(format = 'csv') {
    // This would be implemented with actual export functionality
    console.log(`Exporting transaction history as ${format}`);
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + D: Go to deposit page
    if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
        e.preventDefault();
        window.location.href = '/savings/deposit/';
    }
    
    // Ctrl/Cmd + W: Go to withdraw page
    if ((e.ctrlKey || e.metaKey) && e.key === 'w') {
        e.preventDefault();
        window.location.href = '/savings/withdraw/';
    }
    
    // Ctrl/Cmd + H: Go to transaction history
    if ((e.ctrlKey || e.metaKey) && e.key === 'h') {
        e.preventDefault();
        window.location.href = '/savings/transaction-history/';
    }
});

// Dark mode toggle (placeholder for future implementation)
// (implemented above via initializeTheme)
