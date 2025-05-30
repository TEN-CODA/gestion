// Fonction pour marquer l'élément actif dans le menu
function setActiveMenu() {
    const currentPage = window.location.pathname.split('/').pop();
    const menuItems = document.querySelectorAll('.sidebar-menu li');
    
    menuItems.forEach(item => {
        const link = item.querySelector('a').getAttribute('href');
        if (link === currentPage || (currentPage === '' && link === 'index.html')) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
}

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    setActiveMenu();
    
    // Gestion du formulaire d'ajout d'élève
    const addStudentForm = document.getElementById('addStudentForm');
    if (addStudentForm) {
        addStudentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const name = document.getElementById('studentName').value;
            const studentClass = document.getElementById('studentClass').value;
            
            alert(`Élève ${name} (${studentClass}) ajouté avec succès !`);
            this.reset();
        });
    }
});