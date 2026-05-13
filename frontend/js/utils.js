/**
 * JINJA SSS PLATFORM - UTILITY FUNCTIONS
 * Reusable helper functions for all dashboards
 */

// ============================================
// DOM MANIPULATION HELPERS
// ============================================

/**
 * Select a single DOM element
 * @param {string} selector - CSS selector
 * @param {Element} parent - Parent element (default: document)
 * @returns {Element|null}
 */
function $(selector, parent = document) {
    return parent.querySelector(selector);
}

/**
 * Select multiple DOM elements
 * @param {string} selector - CSS selector
 * @param {Element} parent - Parent element (default: document)
 * @returns {NodeList}
 */
function $$(selector, parent = document) {
    return parent.querySelectorAll(selector);
}

// ============================================
// FORMATTING HELPERS
// ============================================

/**
 * Format a number with commas (e.g., 1234567 -> 1,234,567)
 * @param {number} num
 * @returns {string}
 */
function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

/**
 * Format currency in UGX
 * @param {number} amount
 * @returns {string}
 */
function formatCurrency(amount) {
    return 'UGX ' + new Intl.NumberFormat().format(amount);
}

/**
 * Format a date to a readable string
 * @param {string|Date} date
 * @param {object} options - Intl.DateTimeFormat options
 * @returns {string}
 */
function formatDate(date, options = {}) {
    const defaultOptions = {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };
    return new Date(date).toLocaleDateString('en-UG', { ...defaultOptions, ...options });
}

/**
 * Format time to 12-hour format
 * @param {string} time - Time string (e.g., "14:30")
 * @returns {string}
 */
function formatTime(time) {
    const [hours, minutes] = time.split(':');
    const h = parseInt(hours);
    const ampm = h >= 12 ? 'PM' : 'AM';
    const displayHour = h % 12 || 12;
    return `${displayHour}:${minutes} ${ampm}`;
}

// ============================================
// STORAGE HELPERS
// ============================================

/**
 * Save data to localStorage
 * @param {string} key
 * @param {*} value
 */
function saveToStorage(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
        console.warn('LocalStorage not available:', e);
    }
}

/**
 * Get data from localStorage
 * @param {string} key
 * @param {*} defaultValue
 * @returns {*}
 */
function getFromStorage(key, defaultValue = null) {
    try {
        const value = localStorage.getItem(key);
        return value ? JSON.parse(value) : defaultValue;
    } catch (e) {
        return defaultValue;
    }
}

/**
 * Remove data from localStorage
 * @param {string} key
 */
function removeFromStorage(key) {
    try {
        localStorage.removeItem(key);
    } catch (e) {
        console.warn('LocalStorage not available:', e);
    }
}

// ============================================
// URL HELPERS
// ============================================

/**
 * Get URL parameter by name
 * @param {string} name
 * @returns {string|null}
 */
function getUrlParam(name) {
    const params = new URLSearchParams(window.location.search);
    return params.get(name);
}

/**
 * Update URL without page reload
 * @param {object} params - Key/value pairs
 */
function updateUrl(params) {
    const url = new URL(window.location);
    Object.entries(params).forEach(([key, value]) => {
        url.searchParams.set(key, value);
    });
    window.history.pushState({}, '', url);
}

// ============================================
// DEBOUNCE & THROTTLE
// ============================================

/**
 * Debounce a function (wait until calls stop)
 * @param {Function} func
 * @param {number} delay - milliseconds
 * @returns {Function}
 */
function debounce(func, delay = 300) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}

/**
 * Throttle a function (limit call rate)
 * @param {Function} func
 * @param {number} limit - milliseconds
 * @returns {Function}
 */
function throttle(func, limit = 300) {
    let inThrottle;
    return function (...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => (inThrottle = false), limit);
        }
    };
}

// ============================================
// DELAY
// ============================================

/**
 * Delay execution (async sleep)
 * @param {number} ms - milliseconds
 * @returns {Promise}
 */
function delay(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

// ============================================
// CLIPBOARD
// ============================================

/**
 * Copy text to clipboard
 * @param {string} text
 * @returns {Promise<boolean>}
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        return true;
    } catch (e) {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        return true;
    }
}

// ============================================
// DARK MODE
// ============================================

/**
 * Toggle dark mode
 */
function toggleDarkMode() {
    document.documentElement.classList.toggle('dark');
    const isDark = document.documentElement.classList.contains('dark');
    saveToStorage('darkMode', isDark);
}

/**
 * Initialize dark mode from saved preference
 */
function initDarkMode() {
    const saved = getFromStorage('darkMode');
    if (saved === true) {
        document.documentElement.classList.add('dark');
    } else if (saved === null) {
        // Check system preference
        if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.classList.add('dark');
        }
    }
}

// ============================================
// RESPONSIVE HELPERS
// ============================================

/**
 * Check if current device is mobile
 * @returns {boolean}
 */
function isMobile() {
    return window.innerWidth < 768;
}

/**
 * Check if current device is tablet
 * @returns {boolean}
 */
function isTablet() {
    return window.innerWidth >= 768 && window.innerWidth < 1024;
}

/**
 * Check if current device is desktop
 * @returns {boolean}
 */
function isDesktop() {
    return window.innerWidth >= 1024;
}

// ============================================
// INITIALIZATION
// ============================================

console.log('Jinja SSS Platform - Utils loaded');