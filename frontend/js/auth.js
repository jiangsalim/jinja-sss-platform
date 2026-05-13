/**
 * JINJA SSS PLATFORM - AUTHENTICATION
 * Handles login, logout, token management, session
 */

// ============================================
// AUTH STATE
// ============================================

/**
 * Check if user is logged in
 * @returns {boolean}
 */
function isLoggedIn() {
    return !!getToken();
}

/**
 * Get current user from stored data
 * @returns {object|null}
 */
function getCurrentUser() {
    return getFromStorage('currentUser');
}

/**
 * Get user role
 * @returns {string|null}
 */
function getUserRole() {
    const user = getCurrentUser();
    return user ? user.role : null;
}

// ============================================
// LOGIN
// ============================================

/**
 * Sign in user
 * @param {string} identifier - ID, email, or username
 * @param {string} password
 * @returns {Promise<object>}
 */
async function signIn(identifier, password) {
    const response = await api.post('/auth/login', {
        identifier: identifier,
        password: password
    });
    
    if (response.token) {
        saveToStorage('authToken', response.token);
        saveToStorage('currentUser', response.user);
    }
    
    return response;
}

// ============================================
// PASSWORD CHANGE (First Login)
// ============================================

/**
 * Change password on first login
 * @param {string} currentPassword
 * @param {string} newPassword
 * @returns {Promise<object>}
 */
async function changeFirstPassword(currentPassword, newPassword) {
    const response = await api.post('/auth/change-password', {
        current_password: currentPassword,
        new_password: newPassword
    });
    
    return response;
}

// ============================================
// LOGOUT
// ============================================

/**
 * Logout user
 */
function logout() {
    removeFromStorage('authToken');
    removeFromStorage('currentUser');
    window.location.href = '/pages/signin.html';
}

// ============================================
// SESSION CHECK
// ============================================

/**
 * Check if session is valid
 * @returns {Promise<boolean>}
 */
async function checkSession() {
    if (!isLoggedIn()) return false;
    
    try {
        await api.get('/auth/me');
        return true;
    } catch (error) {
        return false;
    }
}

// ============================================
// REDIRECT IF NOT LOGGED IN
// ============================================

/**
 * Redirect to login if not authenticated
 */
function requireAuth() {
    if (!isLoggedIn()) {
        window.location.href = '/pages/signin.html';
        return false;
    }
    return true;
}

/**
 * Redirect to dashboard if already logged in
 * (for pages like Sign In that shouldn't show if authenticated)
 */
function redirectIfLoggedIn() {
    if (isLoggedIn()) {
        window.location.href = '/pages/dashboard.html';
        return true;
    }
    return false;
}

// ============================================
// INITIALIZATION
// ============================================

// Initialize dark mode on auth pages too
initDarkMode();

console.log('Jinja SSS Platform - Auth loaded');