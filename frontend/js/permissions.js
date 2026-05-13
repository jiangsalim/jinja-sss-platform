/**
 * Jinja SSS Platform - Frontend Permission Checks
 */

let userPermissions = [];

async function loadPermissions() {
    try {
        const response = await api.get('/auth/me');
        userPermissions = response.permissions || [];
        applyPermissions();
    } catch (e) {
        console.warn('Could not load permissions');
    }
}

function hasPermission(resource, action) {
    return userPermissions.includes(`${action}:${resource}`);
}

function applyPermissions() {
    document.querySelectorAll('[data-permission]').forEach(el => {
        const perm = el.dataset.permission;
        if (!hasPermission(perm, 'read')) {
            el.style.display = 'none';
        }
    });
    document.querySelectorAll('[data-permission-action]').forEach(el => {
        const perm = el.dataset.permissionAction;
        if (!hasPermission(perm, 'write')) {
            el.disabled = true;
            el.classList.add('jss-btn--disabled');
        }
    });
}

console.log('Jinja SSS Platform - Permissions loaded');
