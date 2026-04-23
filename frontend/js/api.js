/**
 * JINJA SSS PLATFORM - API CLIENT
 * Handles all communication with the backend
 */

// ============================================
// CONFIGURATION
// ============================================

const API_BASE_URL = 'http://localhost:8000';
const API_TIMEOUT = 30000; // 30 seconds

// ============================================
// CORE API FUNCTIONS
// ============================================

/**
 * Get the authentication token
 * @returns {string|null}
 */
function getToken() {
    return getFromStorage('authToken');
}

/**
 * Make an API request
 * @param {string} endpoint - API endpoint (e.g., '/students/grades')
 * @param {object} options - Fetch options
 * @returns {Promise<object>}
 */
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
            ...options,
            headers,
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        // Handle 401 - redirect to login
        if (response.status === 401) {
            removeFromStorage('authToken');
            window.location.href = '/pages/signin.html';
            return null;
        }
        
        // Parse response
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || `HTTP ${response.status}`);
        }
        
        return data;
        
    } catch (error) {
        clearTimeout(timeoutId);
        
        if (error.name === 'AbortError') {
            throw new Error('Request timed out. Please check your connection.');
        }
        
        if (error.message === 'Failed to fetch') {
            throw new Error('Network error. Please check your internet connection.');
        }
        
        throw error;
    }
}

// ============================================
// HTTP METHOD SHORTCUTS
// ============================================

const api = {
    /**
     * GET request
     */
    get(endpoint) {
        return apiRequest(endpoint, { method: 'GET' });
    },
    
    /**
     * POST request
     */
    post(endpoint, data) {
        return apiRequest(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    /**
     * PUT request
     */
    put(endpoint, data) {
        return apiRequest(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    
    /**
     * PATCH request
     */
    patch(endpoint, data) {
        return apiRequest(endpoint, {
            method: 'PATCH',
            body: JSON.stringify(data)
        });
    },
    
    /**
     * DELETE request
     */
    delete(endpoint) {
        return apiRequest(endpoint, { method: 'DELETE' });
    },
    
    /**
     * Upload file
     */
    async upload(endpoint, formData) {
        const token = getToken();
        
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: token ? { 'Authorization': `Bearer ${token}` } : {},
            body: formData
        });
        
        if (response.status === 401) {
            removeFromStorage('authToken');
            window.location.href = '/pages/signin.html';
            return null;
        }
        
        return response.json();
    }
};

// ============================================
// INITIALIZATION
// ============================================

console.log('Jinja SSS Platform - API Client loaded');