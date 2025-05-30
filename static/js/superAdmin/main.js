// Gestion des écoles
function showAddSchoolModal() {
    document.getElementById('addSchoolModal').style.display = 'block';
}

function closeAddSchoolModal() {
    document.getElementById('addSchoolModal').style.display = 'none';
}

function editSchool(schoolId) {
    // Récupérer les informations de l'école
    fetch(`/api/ecoles/${schoolId}`)
        .then(response => response.json())
        .then(data => {
            // Remplir le formulaire avec les données
            document.getElementById('schoolName').value = data.nom;
            document.getElementById('schoolAddress').value = data.adresse;
            document.getElementById('schoolPhone').value = data.telephone;
            document.getElementById('schoolEmail').value = data.email;
            
            // Afficher le modal
            showAddSchoolModal();
        })
        .catch(error => console.error('Erreur:', error));
}

function deleteSchool(schoolId) {
    if (confirm('Êtes-vous sûr de vouloir supprimer cette école ?')) {
        fetch(`/api/ecoles/${schoolId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                // Supprimer l'élément du DOM
                const schoolElement = document.querySelector(`[data-school-id="${schoolId}"]`);
                if (schoolElement) {
                    schoolElement.remove();
                }
                showNotification('École supprimée avec succès', 'success');
            } else {
                throw new Error('Erreur lors de la suppression');
            }
        })
        .catch(error => {
            console.error('Erreur:', error);
            showNotification('Erreur lors de la suppression', 'error');
        });
    }
}

// Gestion du formulaire d'ajout/modification d'école
document.getElementById('addSchoolForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('nom', document.getElementById('schoolName').value);
    formData.append('adresse', document.getElementById('schoolAddress').value);
    formData.append('telephone', document.getElementById('schoolPhone').value);
    formData.append('email', document.getElementById('schoolEmail').value);
    
    const logoFile = document.getElementById('schoolLogo').files[0];
    if (logoFile) {
        formData.append('logo', logoFile);
    }
    
    // Envoyer les données au serveur
    fetch('/api/ecoles', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        closeAddSchoolModal();
        showNotification('École ajoutée avec succès', 'success');
        // Rafraîchir la liste des écoles
        loadSchools();
    })
    .catch(error => {
        console.error('Erreur:', error);
        showNotification('Erreur lors de l\'ajout de l\'école', 'error');
    });
});

// Chargement des écoles
function loadSchools() {
    fetch('/api/ecoles')
        .then(response => response.json())
        .then(data => {
            const schoolsList = document.querySelector('.schools-list');
            schoolsList.innerHTML = '';
            
            data.forEach(school => {
                const schoolElement = createSchoolElement(school);
                schoolsList.appendChild(schoolElement);
            });
        })
        .catch(error => console.error('Erreur:', error));
}

// Création d'un élément école
function createSchoolElement(school) {
    const div = document.createElement('div');
    div.className = 'school-item';
    div.dataset.schoolId = school.id;
    
    div.innerHTML = `
        <div class="school-info">
            <img src="${school.logo_url || 'https://via.placeholder.com/80'}" alt="${school.nom}">
            <div class="school-details">
                <h3>${school.nom}</h3>
                <p><i class="fas fa-map-marker-alt"></i> ${school.adresse}</p>
                <p><i class="fas fa-phone"></i> ${school.telephone}</p>
            </div>
        </div>
        <div class="school-stats">
            <div class="stat">
                <span class="stat-label">Élèves</span>
                <span class="stat-value">${school.nombre_eleves}</span>
            </div>
            <div class="stat">
                <span class="stat-label">Professeurs</span>
                <span class="stat-value">${school.nombre_professeurs}</span>
            </div>
            <div class="stat">
                <span class="stat-label">Classes</span>
                <span class="stat-value">${school.nombre_classes}</span>
            </div>
        </div>
        <div class="school-actions">
            <button class="btn btn-primary" onclick="editSchool(${school.id})">
                <i class="fas fa-edit"></i> Modifier
            </button>
            <button class="btn btn-danger" onclick="deleteSchool(${school.id})">
                <i class="fas fa-trash"></i> Supprimer
            </button>
        </div>
    `;
    
    return div;
}

// Gestion des notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${getNotificationIcon(type)}"></i>
            <span>${message}</span>
        </div>
        <button class="close-notification" onclick="this.parentElement.remove()">&times;</button>
    `;
    
    document.body.appendChild(notification);
    
    // Supprimer la notification après 5 secondes
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

function getNotificationIcon(type) {
    switch (type) {
        case 'success':
            return 'fa-check-circle';
        case 'error':
            return 'fa-exclamation-circle';
        case 'warning':
            return 'fa-exclamation-triangle';
        default:
            return 'fa-info-circle';
    }
}

// Gestion de la recherche
const searchInput = document.querySelector('.search-box input');
searchInput.addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const schoolItems = document.querySelectorAll('.school-item');
    
    schoolItems.forEach(item => {
        const schoolName = item.querySelector('h3').textContent.toLowerCase();
        const schoolAddress = item.querySelector('.school-details p').textContent.toLowerCase();
        
        if (schoolName.includes(searchTerm) || schoolAddress.includes(searchTerm)) {
            item.style.display = 'flex';
        } else {
            item.style.display = 'none';
        }
    });
});

// Gestion de la pagination
function changePage(page) {
    fetch(`/api/ecoles?page=${page}`)
        .then(response => response.json())
        .then(data => {
            // Mettre à jour la liste des écoles
            const schoolsList = document.querySelector('.schools-list');
            schoolsList.innerHTML = '';
            
            data.ecoles.forEach(school => {
                const schoolElement = createSchoolElement(school);
                schoolsList.appendChild(schoolElement);
            });
            
            // Mettre à jour la pagination
            updatePagination(data.pagination);
        })
        .catch(error => console.error('Erreur:', error));
}

function updatePagination(pagination) {
    const paginationElement = document.querySelector('.pagination');
    paginationElement.innerHTML = '';
    
    // Bouton précédent
    if (pagination.currentPage > 1) {
        paginationElement.innerHTML += `
            <button class="btn btn-outline" onclick="changePage(${pagination.currentPage - 1})">
                <i class="fas fa-chevron-left"></i>
            </button>
        `;
    }
    
    // Numéros de page
    for (let i = 1; i <= pagination.totalPages; i++) {
        paginationElement.innerHTML += `
            <span class="page-number ${i === pagination.currentPage ? 'active' : ''}" 
                  onclick="changePage(${i})">${i}</span>
        `;
    }
    
    // Bouton suivant
    if (pagination.currentPage < pagination.totalPages) {
        paginationElement.innerHTML += `
            <button class="btn btn-outline" onclick="changePage(${pagination.currentPage + 1})">
                <i class="fas fa-chevron-right"></i>
            </button>
        `;
    }
}

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    loadSchools();
}); 