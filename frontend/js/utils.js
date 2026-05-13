/**
 * Jinja SSS Platform - Utilities
 */

function $(selector, parent = document) { return parent.querySelector(selector); }
function $$(selector, parent = document) { return parent.querySelectorAll(selector); }

function formatNumber(num) { return new Intl.NumberFormat().format(num); }
function formatCurrency(amount) { return 'UGX ' + new Intl.NumberFormat().format(amount); }

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-UG', { year: 'numeric', month: 'short', day: 'numeric' });
}

function saveToStorage(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) { console.warn(e); }
}

function getFromStorage(key, defaultValue = null) {
    try {
        const value = localStorage.getItem(key);
        return value ? JSON.parse(value) : defaultValue;
    } catch (e) { return defaultValue; }
}

function showToast(type, message) {
    const toast = document.createElement('div');
    toast.className = `jss-toast jss-toast--${type}`;
    toast.textContent = message;
    toast.style.cssText = 'position:fixed;top:20px;right:20px;padding:12px 20px;border-radius:8px;color:white;z-index:9999;animation:slideIn 0.3s ease;';
    toast.style.background = type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : type === 'warning' ? '#ffc107' : '#17a2b8';
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}

function debounce(func, delay = 300) {
    let timeout;
    return function (...args) { clearTimeout(timeout); timeout = setTimeout(() => func.apply(this, args), delay); };
}

function isOnline() { return navigator.onLine; }

console.log('Jinja SSS Platform - Utils loaded');
