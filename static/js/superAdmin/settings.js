// Profile Form Handling
document.getElementById('profileForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('name', document.getElementById('profileName').value);
    formData.append('email', document.getElementById('profileEmail').value);
    formData.append('phone', document.getElementById('profilePhone').value);
    
    const photoFile = document.getElementById('profilePhoto').files[0];
    if (photoFile) {
        formData.append('photo', photoFile);
    }

    try {
        const response = await fetch('/api/profile', {
            method: 'PUT',
            body: formData
        });

        if (response.ok) {
            showNotification('Profil mis à jour avec succès', 'success');
        } else {
            throw new Error('Erreur lors de la mise à jour du profil');
        }
    } catch (error) {
        showNotification(error.message, 'error');
    }
});

// Security Form Handling
document.getElementById('securityForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const twoFactorAuth = document.getElementById('twoFactorAuth').checked;

    if (newPassword !== confirmPassword) {
        showNotification('Les mots de passe ne correspondent pas', 'error');
        return;
    }

    try {
        const response = await fetch('/api/security', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                currentPassword,
                newPassword,
                twoFactorAuth
            })
        });

        if (response.ok) {
            showNotification('Paramètres de sécurité mis à jour', 'success');
            document.getElementById('securityForm').reset();
        } else {
            throw new Error('Erreur lors de la mise à jour des paramètres de sécurité');
        }
    } catch (error) {
        showNotification(error.message, 'error');
    }
});

// Notifications Form Handling
document.getElementById('notificationsForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const notificationSettings = {
        email: document.getElementById('emailNotifications').checked,
        sms: document.getElementById('smsNotifications').checked,
        newUsers: document.getElementById('newUserNotifications').checked,
        support: document.getElementById('supportNotifications').checked,
        system: document.getElementById('systemNotifications').checked
    };

    try {
        const response = await fetch('/api/notifications', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(notificationSettings)
        });

        if (response.ok) {
            showNotification('Préférences de notifications mises à jour', 'success');
        } else {
            throw new Error('Erreur lors de la mise à jour des préférences de notifications');
        }
    } catch (error) {
        showNotification(error.message, 'error');
    }
});

// System Settings Form Handling
document.getElementById('systemForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const systemSettings = {
        language: document.getElementById('language').value,
        timezone: document.getElementById('timezone').value,
        dateFormat: document.getElementById('dateFormat').value,
        maintenanceMode: document.getElementById('maintenanceMode').checked
    };

    try {
        const response = await fetch('/api/system', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(systemSettings)
        });

        if (response.ok) {
            showNotification('Paramètres système mis à jour', 'success');
            if (systemSettings.maintenanceMode) {
                showNotification('Le mode maintenance a été activé', 'warning');
            }
        } else {
            throw new Error('Erreur lors de la mise à jour des paramètres système');
        }
    } catch (error) {
        showNotification(error.message, 'error');
    }
});

// Load User Settings
async function loadUserSettings() {
    try {
        const response = await fetch('/api/settings');
        if (response.ok) {
            const settings = await response.json();
            
            // Populate Profile
            document.getElementById('profileName').value = settings.profile.name;
            document.getElementById('profileEmail').value = settings.profile.email;
            document.getElementById('profilePhone').value = settings.profile.phone;

            // Populate Security
            document.getElementById('twoFactorAuth').checked = settings.security.twoFactorAuth;

            // Populate Notifications
            document.getElementById('emailNotifications').checked = settings.notifications.email;
            document.getElementById('smsNotifications').checked = settings.notifications.sms;
            document.getElementById('newUserNotifications').checked = settings.notifications.newUsers;
            document.getElementById('supportNotifications').checked = settings.notifications.support;
            document.getElementById('systemNotifications').checked = settings.notifications.system;

            // Populate System
            document.getElementById('language').value = settings.system.language;
            document.getElementById('timezone').value = settings.system.timezone;
            document.getElementById('dateFormat').value = settings.system.dateFormat;
            document.getElementById('maintenanceMode').checked = settings.system.maintenanceMode;
        }
    } catch (error) {
        showNotification('Erreur lors du chargement des paramètres', 'error');
    }
}

// Notification Helper Function
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadUserSettings();
}); 