/**
 * JINJA SSS PLATFORM - FORM VALIDATION
 * Standard validation functions for all forms
 */

// ============================================
// VALIDATION RULES
// ============================================

const VALIDATION_RULES = {
    required: {
        test: (value) => value !== null && value !== undefined && value.toString().trim() !== '',
        message: 'This field is required.'
    },
    email: {
        test: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
        message: 'Please enter a valid email address.'
    },
    phone: {
        test: (value) => /^0\d{9}$/.test(value.replace(/\s/g, '')),
        message: 'Please enter a valid phone number (e.g., 0700000000).'
    },
    password: {
        test: (value) => value.length >= 6,
        message: 'Password must be at least 6 characters.'
    },
    admissionNumber: {
        test: (value) => /^JSSS-\d{3}$/.test(value),
        message: 'Please enter a valid admission number (e.g., JSSS-001).'
    },
    staffId: {
        test: (value) => /^[A-Z]{3}-\d{3}$/.test(value),
        message: 'Please enter a valid staff ID (e.g., TCH-001).'
    }
};

// ============================================
// VALIDATE SINGLE INPUT
// ============================================

/**
 * Validate a single input element
 * @param {HTMLInputElement} input
 * @returns {object} { valid: boolean, message: string }
 */
function validateInput(input) {
    const rules = input.dataset.validate ? input.dataset.validate.split(' ') : [];
    
    for (const rule of rules) {
        if (rule === 'required' && input.hasAttribute('data-required-if')) {
            // Skip required validation based on condition
            continue;
        }
        
        if (VALIDATION_RULES[rule] && !VALIDATION_RULES[rule].test(input.value)) {
            return {
                valid: false,
                message: input.dataset.message || VALIDATION_RULES[rule].message
            };
        }
    }
    
    return { valid: true, message: '' };
}

// ============================================
// SHOW / CLEAR ERROR
// ============================================

/**
 * Show error on an input
 * @param {HTMLInputElement} input
 * @param {string} message
 */
function showInputError(input, message) {
    // Add error class to input
    input.classList.add('jss-input--error');
    
    // Find or create error message element
    let errorElement = input.parentElement.querySelector('.jss-error-message');
    
    if (!errorElement) {
        errorElement = document.createElement('span');
        errorElement.className = 'jss-error-message';
        input.parentElement.appendChild(errorElement);
    }
    
    errorElement.textContent = message;
}

/**
 * Clear error on an input
 * @param {HTMLInputElement} input
 */
function clearInputError(input) {
    input.classList.remove('jss-input--error');
    
    const errorElement = input.parentElement.querySelector('.jss-error-message');
    if (errorElement) {
        errorElement.remove();
    }
}

// ============================================
// VALIDATE FORM
// ============================================

/**
 * Validate an entire form
 * @param {HTMLFormElement} form
 * @returns {boolean}
 */
function validateForm(form) {
    let isValid = true;
    
    const inputs = form.querySelectorAll('input[data-validate], select[data-validate], textarea[data-validate]');
    
    inputs.forEach(input => {
        const result = validateInput(input);
        
        if (!result.valid) {
            showInputError(input, result.message);
            isValid = false;
        } else {
            clearInputError(input);
        }
    });
    
    return isValid;
}

// ============================================
// REAL-TIME VALIDATION
// ============================================

/**
 * Attach real-time validation to a form
 * @param {HTMLFormElement} form
 */
function attachValidation(form) {
    const inputs = form.querySelectorAll('input[data-validate], select[data-validate], textarea[data-validate]');
    
    inputs.forEach(input => {
        input.addEventListener('blur', () => {
            const result = validateInput(input);
            if (!result.valid) {
                showInputError(input, result.message);
            } else {
                clearInputError(input);
            }
        });
        
        input.addEventListener('input', () => {
            clearInputError(input);
        });
    });
}

// ============================================
// INITIALIZATION
// ============================================

console.log('Jinja SSS Platform - Validation loaded');