/**
 * Jinja SSS Platform - Authentication Module
 */

async function signIn(identifier, password) {
    const response = await api.post('/auth/signin', { identifier, password });
    if (response.access_token) {
        saveToken(response.access_token);
    }
    return response;
}

async function signUp(userData) {
    return await api.post('/auth/signup', userData);
}

async function changePassword(currentPassword, newPassword) {
    return await api.post('/auth/change-password', {
        current_password: currentPassword,
        new_password: newPassword
    });
}

function isLoggedIn() {
    return !!getToken();
}

function logout() {
    removeToken();
    window.location.href = '/pages/signin.html';
}

function initDarkMode() {
    const saved = localStorage.getItem('darkMode');
    if (saved === 'true') {
        document.documentElement.classList.add('dark');
    }
}

console.log('Jinja SSS Platform - Auth module loaded');
