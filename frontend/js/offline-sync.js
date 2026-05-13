/**
 * Jinja SSS Platform - Offline Sync
 */

class SyncQueue {
    static async add(operation) {
        const queue = getFromStorage('syncQueue', []);
        queue.push({ ...operation, timestamp: Date.now(), retryCount: 0 });
        saveToStorage('syncQueue', queue);
    }

    static async process() {
        if (!navigator.onLine) return;
        const queue = getFromStorage('syncQueue', []);
        const remaining = [];
        for (const item of queue) {
            try {
                await api.post(item.endpoint, item.data);
            } catch (error) {
                item.retryCount++;
                if (item.retryCount < 3) remaining.push(item);
            }
        }
        saveToStorage('syncQueue', remaining);
    }
}

window.addEventListener('online', () => {
    showToast('info', 'Back online! Syncing data...');
    SyncQueue.process();
});

window.addEventListener('offline', () => {
    showToast('warning', 'You are offline. Changes will sync later.');
});

console.log('Jinja SSS Platform - Offline Sync loaded');
