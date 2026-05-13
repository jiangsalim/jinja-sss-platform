/**
 * Jinja SSS Platform - Form Validation
 */

const VALIDATION_RULES = {
    required: { test: (v) => v && v.toString().trim() !== '', message: 'This field is required.' },
    email: { test: (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v), message: 'Please enter a valid email.' },
    phone: { test: (v) => /^0\d{9}$/.test(v), message: 'Please enter a valid phone number.' },
    password: { test: (v) => v && v.length >= 8, message: 'Password must be at least 8 characters.' },
    admission: { test: (v) => /^JSSS-\d{3}$/.test(v), message: 'Invalid admission number (e.g., JSSS-001).' },
    staffId: { test: (v) => /^[A-Z]{3}-\d{3}$/.test(v), message: 'Invalid staff ID (e.g., TCH-001).' },
};

function validateInput(input) {
    const rules = input.dataset.validate ? input.dataset.validate.split(' ') : [];
    for (const rule of rules) {
        if (VALIDATION_RULES[rule] && !VALIDATION_RULES[rule].test(input.value)) {
            return { valid: false, message: VALIDATION_RULES[rule].message };
        }
    }
    return { valid: true, message: '' };
}

function showInputError(input, message) {
    input.classList.add('jss-input--error');
    let error = input.parentElement.querySelector('.jss-error-message');
    if (!error) {
        error = document.createElement('span');
        error.className = 'jss-error-message';
        input.parentElement.appendChild(error);
    }
    error.textContent = message;
}

function clearInputError(input) {
    input.classList.remove('jss-input--error');
    const error = input.parentElement.querySelector('.jss-error-message');
    if (error) error.remove();
}

console.log('Jinja SSS Platform - Validation loaded');
