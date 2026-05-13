/**
 * Jinja SSS Platform - API Client
 * Handles all communication with the backend
 */

const API_BASE_URL = 'http://localhost:9000';
const API_TIMEOUT = 30000;

function getToken() {
    return localStorage.getItem('authToken');
}

function saveToken(token) {
    localStorage.setItem('authToken', token);
}

function removeToken() {
    localStorage.removeItem('authToken');
}

async function apiRequest(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers
    };

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options, headers, signal: controller.signal
        });
        clearTimeout(timeoutId);
        if (response.status === 401) {
            removeToken();
            window.location.href = '/pages/signin.html';
            return null;
        }
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || data.error?.message || `HTTP ${response.status}`);
        }
        return data;
    } catch (error) {
        clearTimeout(timeoutId);
        if (error.name === 'AbortError') {
            throw new Error('Request timed out');
        }
        if (error.message === 'Failed to fetch') {
            throw new Error('Network error');
        }
        throw error;
    }
}

const api = {
    get: (endpoint) => apiRequest(endpoint, { method: 'GET' }),
    post: (endpoint, data) => apiRequest(endpoint, { method: 'POST', body: JSON.stringify(data) }),
    put: (endpoint, data) => apiRequest(endpoint, { method: 'PUT', body: JSON.stringify(data) }),
    patch: (endpoint, data) => apiRequest(endpoint, { method: 'PATCH', body: JSON.stringify(data) }),
    delete: (endpoint) => apiRequest(endpoint, { method: 'DELETE' }),
    upload: async (endpoint, formData) => {
        const token = getToken();
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: token ? { 'Authorization': `Bearer ${token}` } : {},
            body: formData
        });
        return response.json();
    }
};

console.log('Jinja SSS Platform - API Client loaded');
