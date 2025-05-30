// Classe pour gérer les notifications
class NotificationSystem {
    constructor() {
        this.notifications = [];
        this.container = null;
        this.init();
    }

    init() {
        // Créer le conteneur de notifications
        this.container = document.createElement('div');
        this.container.className = 'notifications-container';
        document.body.appendChild(this.container);

        // Ajouter le bouton de notifications dans le header
        const userInfo = document.querySelector('.user-info');
        if (userInfo) {
            const notificationBtn = document.createElement('button');
            notificationBtn.className = 'notification-btn';
            notificationBtn.innerHTML = `
                <i class="fas fa-bell"></i>
                <span class="notification-badge">0</span>
            `;
            userInfo.insertBefore(notificationBtn, userInfo.firstChild);

            // Ajouter le panneau de notifications
            const notificationPanel = document.createElement('div');
            notificationPanel.className = 'notification-panel';
            notificationPanel.innerHTML = `
                <div class="notification-header">
                    <h3>Notifications</h3>
                    <button class="mark-all-read">Tout marquer comme lu</button>
                </div>
                <div class="notification-list"></div>
            `;
            userInfo.appendChild(notificationPanel);

            // Gérer les événements
            notificationBtn.addEventListener('click', () => {
                this.showNotificationsModal();
            });

            document.addEventListener('click', (e) => {
                if (!notificationBtn.contains(e.target) && !notificationPanel.contains(e.target)) {
                    notificationPanel.classList.remove('active');
                }
            });

            // Marquer toutes les notifications comme lues
            notificationPanel.querySelector('.mark-all-read').addEventListener('click', () => {
                this.markAllAsRead();
            });
        }
    }

    addNotification(notification) {
        this.notifications.unshift({
            ...notification,
            id: Date.now(),
            read: false,
            time: new Date()
        });

        this.updateUI();
        this.showToast(notification);
    }

    markAsRead(id) {
        const notification = this.notifications.find(n => n.id === id);
        if (notification) {
            notification.read = true;
            this.updateUI();
        }
    }

    markAllAsRead() {
        this.notifications.forEach(notification => {
            notification.read = true;
        });
        this.updateUI();
    }

    updateUI() {
        // Mettre à jour le badge
        const badge = document.querySelector('.notification-badge');
        const unreadCount = this.notifications.filter(n => !n.read).length;
        badge.textContent = unreadCount;
        badge.style.display = unreadCount > 0 ? 'block' : 'none';
        
        // Ajouter la classe has-new si il y a des notifications non lues
        if (unreadCount > 0) {
            badge.classList.add('has-new');
        } else {
            badge.classList.remove('has-new');
        }

        // Mettre à jour la liste des notifications
        const notificationList = document.querySelector('.notification-list');
        if (notificationList) {
            notificationList.innerHTML = this.notifications.length ? this.notifications.map(notification => `
                <div class="notification-item ${notification.read ? 'read' : ''}" data-id="${notification.id}">
                    <div class="notification-icon">
                        <i class="fas fa-${this.getIconForType(notification.type)}"></i>
                    </div>
                    <div class="notification-content">
                        <div class="notification-title">${notification.title}</div>
                        <div class="notification-message">${notification.message}</div>
                        <div class="notification-time">${this.formatTime(notification.time)}</div>
                    </div>
                    ${!notification.read ? '<div class="notification-dot"></div>' : ''}
                </div>
            `).join('') : '<div class="no-notifications">Aucune notification</div>';

            // Ajouter les événements de clic
            notificationList.querySelectorAll('.notification-item').forEach(item => {
                item.addEventListener('click', () => {
                    this.markAsRead(parseInt(item.dataset.id));
                    if (notification.action) {
                        notification.action();
                    }
                });
            });
        }
    }

    showToast(notification) {
        const toast = document.createElement('div');
        toast.className = `notification-toast notification-${notification.type}`;
        toast.innerHTML = `
            <i class="fas fa-${this.getIconForType(notification.type)}"></i>
            <div class="toast-content">
                <div class="toast-title">${notification.title}</div>
                <div class="toast-message">${notification.message}</div>
            </div>
        `;

        this.container.appendChild(toast);
        setTimeout(() => toast.classList.add('show'), 10);
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    }

    getIconForType(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-circle',
            warning: 'exclamation-triangle',
            info: 'info-circle',
            message: 'envelope',
            user: 'user',
            school: 'school',
            report: 'chart-bar'
        };
        return icons[type] || 'bell';
    }

    formatTime(date) {
        const now = new Date();
        const diff = now - date;
        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);

        if (minutes < 60) {
            return `Il y a ${minutes} min`;
        } else if (hours < 24) {
            return `Il y a ${hours} h`;
        } else if (days < 7) {
            return `Il y a ${days} j`;
        } else {
            return date.toLocaleDateString();
        }
    }

    showNotificationsModal() {
        ModalManager.create({
            title: 'Notifications',
            content: `
                <div class="notifications-modal-content">
                    <div class="notifications-header">
                        <button class="mark-all-read">Tout marquer comme lu</button>
                    </div>
                    <div class="notifications-list">
                        ${this.notifications.length ? this.notifications.map(notification => `
                            <div class="notification-item ${notification.read ? 'read' : ''}" data-id="${notification.id}">
                                <div class="notification-icon">
                                    <i class="fas fa-${this.getIconForType(notification.type)}"></i>
                                </div>
                                <div class="notification-content">
                                    <div class="notification-title">${notification.title}</div>
                                    <div class="notification-message">${notification.message}</div>
                                    <div class="notification-time">${this.formatTime(notification.time)}</div>
                                </div>
                                ${!notification.read ? '<div class="notification-dot"></div>' : ''}
                            </div>
                        `).join('') : '<div class="no-notifications">Aucune notification</div>'}
                    </div>
                </div>
            `,
            size: 'medium',
            buttons: [
                {
                    text: 'Fermer',
                    icon: 'times',
                    action: 'close'
                }
            ]
        });

        // Ajouter les événements de clic
        const notificationList = document.querySelector('.notifications-list');
        if (notificationList) {
            notificationList.querySelectorAll('.notification-item').forEach(item => {
                item.addEventListener('click', () => {
                    this.markAsRead(parseInt(item.dataset.id));
                    if (this.notifications.find(n => n.id === parseInt(item.dataset.id))?.action) {
                        this.notifications.find(n => n.id === parseInt(item.dataset.id)).action();
                    }
                });
            });
        }

        // Gérer le bouton "Tout marquer comme lu"
        const markAllReadBtn = document.querySelector('.mark-all-read');
        if (markAllReadBtn) {
            markAllReadBtn.addEventListener('click', () => {
                this.markAllAsRead();
                this.updateUI();
            });
        }
    }
}

// Initialiser le système de notifications
window.NotificationSystem = new NotificationSystem();

// Exemple d'utilisation :
/*
NotificationSystem.addNotification({
    type: 'success',
    title: 'Nouvelle école ajoutée',
    message: 'L\'école "Lycée Descartes" a été ajoutée avec succès.',
    action: () => {
        // Action à effectuer lors du clic sur la notification
        window.location.href = 'ecoles.html';
    }
});
*/ 