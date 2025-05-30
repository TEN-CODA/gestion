 // Fonctions supplémentaires pour les parents
 function viewMessageDetails() {
    showModal('message-modal');
}

function downloadDocument(docId) {
    // Simuler le téléchargement
    alert('Téléchargement du document ' + docId + ' en cours...');
}

function requestMeeting() {
    showTab('messages');
    showInnerTab('send-message');
    // Pré-remplir le formulaire avec le destinataire "Professeur principal"
    document.querySelector('#send-message select').value = "Professeur principal";
    window.scrollTo(0, 0);
}

// Amélioration de la fonction showTab pour gérer les sous-onglets
function showTab(tabId) {
    // Masquer tous les contenus d'onglets
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Afficher l'onglet sélectionné
    const tab = document.getElementById(tabId);
    tab.classList.add('active');
    
    // Activer le premier sous-onglet s'il existe
    const firstInnerTab = tab.querySelector('.inner-tab-content');
    if (firstInnerTab) {
        firstInnerTab.classList.add('active');
        
        // Activer le premier onglet dans le groupe
        const firstTab = tab.querySelector('.tab');
        if (firstTab) {
            firstTab.classList.add('active');
        }
    }
    
    // Mettre à jour le titre de la page
    updatePageTitle(tabId);
    
    // Mettre à jour le menu actif
    updateActiveMenu(tabId);
}

function updatePageTitle(tabId) {
    const tabTitles = {
        'dashboard': 'Tableau de Bord',
        'children': 'Mes Enfants',
        'payments': 'Paiements',
        'messages': 'Messagerie',
        'performance': 'Performances',
        'schedule': 'Emploi du temps',
        'exams': 'Contrôles',
        'calendar': 'Calendrier',
        'behavior-reports': 'Comportement',
        'documents': 'Documents',
        'settings': 'Paramètres'
    };
    document.getElementById('page-title').textContent = tabTitles[tabId] || 'Tableau de Bord';
}

function updateActiveMenu(tabId) {
    document.querySelectorAll('.sidebar-menu a').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('onclick')?.includes(tabId)) {
            link.classList.add('active');
        }
    });
}

// Initialisation des événements
document.addEventListener('DOMContentLoaded', function() {
    // Gestion des clics sur les messages
    document.querySelectorAll('#inbox button').forEach(btn => {
        btn.addEventListener('click', viewMessageDetails);
    });
    
    // Gestion des téléchargements de documents
    document.querySelectorAll('.activity-list button').forEach(btn => {
        if (btn.textContent.includes('Télécharger')) {
            btn.addEventListener('click', function() {
                const docName = this.closest('.activity-item').querySelector('h4').textContent;
                downloadDocument(docName);
            });
        }
    });
    
    // Activer le premier onglet par défaut
    showTab('dashboard');
});


let notifs=document.querySelectorAll('.activity-content');
let msgModal=document.getElementById('message-modal');
let close=msgModal.querySelector('.close');
notifs.forEach(e =>{
    e.addEventListener('click',()=>{
        msgModal.style.display='flex';
        close.addEventListener('click',()=>{
            msgModal.style.display='none';
            
        })
    })
})