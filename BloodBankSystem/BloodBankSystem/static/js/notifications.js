// Notifications WebSocket functionality
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize if user is logged in
    if (document.getElementById('notification-badge')) {
        initializeWebSocket();
    }
});

function initializeWebSocket() {
    // Get user ID from meta tag
    const userId = document.querySelector('meta[name="user-id"]').getAttribute('content');
    
    if (!userId) {
        console.error('User ID not found');
        return;
    }
    
    // Create WebSocket connection
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/ws/notifications/${userId}/`;
    
    const socket = new WebSocket(wsUrl);
    
    socket.onopen = function(e) {
        console.log('WebSocket connection established');
    };
    
    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        
        if (data.type === 'new_notification') {
            // Show notification
            showNotification(data.message, data.notification_type);
            
            // Update notification badge
            updateNotificationBadge(1);
            
            // Refresh the page if we're on the notifications page
            if (window.location.pathname.includes('/notifications/')) {
                window.location.reload();
            }
        } else if (data.type === 'notification_list') {
            // Update notification list if we're on the notifications page
            if (window.location.pathname.includes('/notifications/')) {
                updateNotificationList(data.notifications);
            }
        }
    };
    
    socket.onclose = function(e) {
        console.error('WebSocket connection closed unexpectedly');
        // Try to reconnect after 5 seconds
        setTimeout(initializeWebSocket, 5000);
    };
    
    socket.onerror = function(e) {
        console.error('WebSocket error:', e);
    };
}

function showNotification(message, type) {
    // Create notification toast
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    // Set icon and color based on notification type
    let icon = 'bell';
    let bgColor = 'bg-primary';
    
    if (type === 'blood_request') {
        icon = 'tint';
        bgColor = 'bg-danger';
    } else if (type === 'donor_available') {
        icon = 'user';
        bgColor = 'bg-success';
    } else if (type === 'request_fulfilled') {
        icon = 'check-circle';
        bgColor = 'bg-success';
    }
    
    toast.innerHTML = `
        <div class="toast-header ${bgColor} text-white">
            <i class="fas fa-${icon} me-2"></i>
            <strong class="me-auto">New Notification</strong>
            <small>Just now</small>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Initialize and show toast
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1050';
    document.body.appendChild(container);
    return container;
}

function updateNotificationBadge(increment) {
    const badge = document.getElementById('notification-badge');
    if (badge) {
        let count = parseInt(badge.textContent.trim()) || 0;
        count += increment;
        
        if (count > 0) {
            badge.textContent = count;
            badge.style.display = 'inline-block';
        } else {
            badge.style.display = 'none';
        }
    }
}

function updateNotificationList(notifications) {
    const listContainer = document.getElementById('notification-list');
    if (!listContainer) return;
    
    // Clear existing notifications
    listContainer.innerHTML = '';
    
    if (notifications.length === 0) {
        listContainer.innerHTML = '<div class="alert alert-info">You don\'t have any notifications yet.</div>';
        return;
    }
    
    // Add each notification to the list
    notifications.forEach(notification => {
        const item = document.createElement('div');
        item.className = `list-group-item list-group-item-action ${notification.is_read ? '' : 'list-group-item-warning'}`;
        
        let icon = 'bell';
        if (notification.notification_type === 'blood_request') {
            icon = 'tint text-danger';
        } else if (notification.notification_type === 'donor_available') {
            icon = 'user text-success';
        } else if (notification.notification_type === 'request_fulfilled') {
            icon = 'check-circle text-success';
        }
        
        item.innerHTML = `
            <div class="d-flex w-100 justify-content-between">
                <h5 class="mb-1">
                    <i class="fas fa-${icon}"></i> ${notification.notification_type.replace('_', ' ').toUpperCase()}
                </h5>
                <small>${notification.created_at}</small>
            </div>
            <p class="mb-1">${notification.message}</p>
            <div class="d-flex justify-content-between align-items-center mt-2">
                <div>
                    ${notification.related_request ? 
                        `<a href="/user/my-requests/${notification.related_request}/" class="btn btn-sm btn-info">View Request</a>` : ''}
                </div>
                ${!notification.is_read ? 
                    `<a href="/user/notifications/${notification.id}/mark-read/" class="btn btn-sm btn-outline-secondary">Mark as Read</a>` : ''}
            </div>
        `;
        
        listContainer.appendChild(item);
    });
}
