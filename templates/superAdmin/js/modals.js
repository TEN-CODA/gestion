// Fonction pour créer et afficher un modal
function createModal(options) {
    const {
        title,
        content,
        size = 'medium',
        buttons = [],
        onClose = () => {}
    } = options;

    // Créer l'overlay
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    
    // Créer le modal
    const modal = document.createElement('div');
    modal.className = `modal modal-${size}`;
    
    // Créer l'en-tête
    const header = document.createElement('div');
    header.className = 'modal-header';
    header.innerHTML = `
        <h3>${title}</h3>
        <button class="modal-close">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Créer le contenu
    const body = document.createElement('div');
    body.className = 'modal-body';
    body.innerHTML = content;
    
    // Créer le footer avec les boutons
    const footer = document.createElement('div');
    footer.className = 'modal-footer';
    buttons.forEach(button => {
        const btn = document.createElement('button');
        btn.className = `btn ${button.class || 'btn-outline'}`;
        btn.innerHTML = button.icon ? `<i class="fas fa-${button.icon}"></i> ${button.text}` : button.text;
        if (button.onClick) {
            btn.addEventListener('click', () => {
                button.onClick();
                closeModal();
            });
        }
        footer.appendChild(btn);
    });
    
    // Assembler le modal
    modal.appendChild(header);
    modal.appendChild(body);
    modal.appendChild(footer);
    overlay.appendChild(modal);
    
    // Ajouter au DOM
    document.body.appendChild(overlay);
    
    // Gérer la fermeture
    const closeModal = () => {
        overlay.classList.add('fade-out');
        setTimeout(() => {
            document.body.removeChild(overlay);
            onClose();
        }, 300);
    };
    
    // Événements de fermeture
    overlay.querySelector('.modal-close').addEventListener('click', closeModal);
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) closeModal();
    });
    
    // Animation d'entrée
    setTimeout(() => overlay.classList.add('show'), 10);
    
    return {
        close: closeModal,
        element: modal
    };
}

// Fonction pour afficher un modal de confirmation
function showConfirmModal(options) {
    const {
        title = 'Confirmation',
        message,
        confirmText = 'Confirmer',
        cancelText = 'Annuler',
        onConfirm = () => {},
        onCancel = () => {}
    } = options;

    return createModal({
        title,
        content: `<p>${message}</p>`,
        size: 'small',
        buttons: [
            {
                text: cancelText,
                class: 'btn-outline',
                onClick: onCancel
            },
            {
                text: confirmText,
                class: 'btn-danger',
                icon: 'check',
                onClick: onConfirm
            }
        ]
    });
}

// Fonction pour afficher un modal de détails
function showDetailsModal(options) {
    const {
        title,
        details,
        size = 'large'
    } = options;

    return createModal({
        title,
        content: details,
        size,
        buttons: [
            {
                text: 'Fermer',
                class: 'btn-outline',
                onClick: () => {}
            }
        ]
    });
}

// Fonction pour afficher un modal de formulaire
function showFormModal(options) {
    const {
        title,
        formContent,
        submitText = 'Enregistrer',
        cancelText = 'Annuler',
        onSubmit = () => {},
        onCancel = () => {}
    } = options;

    return createModal({
        title,
        content: formContent,
        size: 'large',
        buttons: [
            {
                text: cancelText,
                class: 'btn-outline',
                onClick: onCancel
            },
            {
                text: submitText,
                class: 'btn-primary',
                icon: 'save',
                onClick: onSubmit
            }
        ]
    });
}

// Fonction pour afficher une notification
function showNotification(message, type = 'success', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, duration);
}

// Exporter les fonctions
window.ModalManager = {
    create: createModal,
    confirm: showConfirmModal,
    details: showDetailsModal,
    form: showFormModal,
    notify: showNotification
}; 