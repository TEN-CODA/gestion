document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initApp();
});

function initApp() {
    // Navigation handling
    setupNavigation();
    
    // School selector handlin
    setupSchoolSelector();
    
    // Modal handling
    setupModals();
    
    // Load initial data
    loadDashboardData();
    loadSchoolsData();
    
    // Initialize charts
    initCharts();
}

function setupNavigation() {
    const navItems = document.querySelectorAll('.sidebar-nav li');
    
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            // Remove active class from all items
            navItems.forEach(navItem => navItem.classList.remove('active'));
            
            // Add active class to clicked item
            this.classList.add('active');
            
            // Hide all sections
            document.querySelectorAll('.content-section').forEach(section => {
                section.classList.remove('active');
            });
            
            // Show the selected section
            const sectionId = this.getAttribute('data-section') + '-section';
            document.getElementById(sectionId).classList.add('active');
        });
    });
}

function setupSchoolSelector() {
    const schoolSelect = document.getElementById('school-select');
    
    // Simulate loading schools from API
    const schools = [
        { id: '1', name: 'École Primaire Les Lilas' },
        { id: '2', name: 'Collège Jean Moulin' },
        { id: '3', name: 'Lycée International' },
        { id: '4', name: 'École Maternelle Arc-en-Ciel' }
    ];
    
    // Populate the select
    schools.forEach(school => {
        const option = document.createElement('option');
        option.value = school.id;
        option.textContent = school.name;
        schoolSelect.appendChild(option);
    });
    
    // Handle school change
    schoolSelect.addEventListener('change', function() {
        const selectedSchoolId = this.value;
        // In a real app, we would reload data based on the selected school
        console.log('Selected school:', selectedSchoolId);
        loadDashboardData(selectedSchoolId);
    });
}

function setupModals() {
    // Add school button
    const addSchoolBtn = document.getElementById('add-school-btn');
    if (addSchoolBtn) {
        addSchoolBtn.addEventListener('click', function() {
            // Reset form
            document.getElementById('school-form').reset();
            document.getElementById('school-id').value = '';
            
            // Show modal
            const modal = new bootstrap.Modal(document.getElementById('school-modal'));
            modal.show();
        });
    }
    
    // Save school button
    const saveSchoolBtn = document.getElementById('save-school-btn');
    if (saveSchoolBtn) {
        saveSchoolBtn.addEventListener('click', function() {
            const form = document.getElementById('school-form');
            if (form.checkValidity()) {
                saveSchool();
            } else {
                form.reportValidity();
            }
        });
    }
}

function saveSchool() {
    const formData = {
        id: document.getElementById('school-id').value,
        name: document.getElementById('school-name').value,
        address: document.getElementById('school-address').value,
        city: document.getElementById('school-city').value,
        phone: document.getElementById('school-phone').value,
        email: document.getElementById('school-email').value,
        status: document.getElementById('school-status').value
    };
    
    console.log('Saving school:', formData);
    
    // In a real app, this would be an API call
    // For now, we'll just close the modal and refresh the schools list
    const modal = bootstrap.Modal.getInstance(document.getElementById('school-modal'));
    modal.hide();
    
    loadSchoolsData();
}

function loadDashboardData(schoolId = 'all') {
    // Simulate API call to get dashboard data
    setTimeout(() => {
        // Update widgets with random data for demo
        document.getElementById('total-students').textContent = schoolId === 'all' ? '1,245' : '325';
        document.getElementById('total-teachers').textContent = schoolId === 'all' ? '78' : '22';
        document.getElementById('total-finances').textContent = schoolId === 'all' ? '124,560€' : '45,230€';
        document.getElementById('attendance-rate').textContent = schoolId === 'all' ? '94%' : '96%';
        
        // Update recent activity
        const activities = [
            { date: '10/05/2023 09:15', school: 'École Primaire Les Lilas', action: 'Connexion', user: 'Admin' },
            { date: '10/05/2023 08:30', school: 'Collège Jean Moulin', action: 'Mise à jour des notes', user: 'Professeur Dupont' },
            { date: '09/05/2023 16:45', school: 'Lycée International', action: 'Paiement enregistré', user: 'Parent Martin' },
            { date: '09/05/2023 14:20', school: 'École Maternelle Arc-en-Ciel', action: 'Ajout élève', user: 'Secrétaire' },
            { date: '09/05/2023 11:10', school: 'Collège Jean Moulin', action: 'Export des données', user: 'Directeur' }
        ];
        
        const activityTable = document.getElementById('recent-activity');
        activityTable.innerHTML = '';
        
        activities.forEach(activity => {
            if (schoolId === 'all' || activity.school === document.getElementById('school-select').options[document.getElementById('school-select').selectedIndex].text) {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${activity.date}</td>
                    <td>${activity.school}</td>
                    <td>${activity.action}</td>
                    <td>${activity.user}</td>
                `;
                activityTable.appendChild(row);
            }
        });
        
        // Update chart
        updateSchoolsStatusChart(schoolId);
    }, 500);
}

function loadSchoolsData() {
    // Simulate API call to get schools data
    setTimeout(() => {
        const schools = [
            { name: 'École Primaire Les Lilas', city: 'Paris', students: 320, teachers: 18, status: 'active' },
            { name: 'Collège Jean Moulin', city: 'Lyon', students: 450, teachers: 32, status: 'active' },
            { name: 'Lycée International', city: 'Marseille', students: 875, teachers: 65, status: 'active' },
            { name: 'École Maternelle Arc-en-Ciel', city: 'Toulouse', students: 120, teachers: 8, status: 'inactive' }
        ];
        
        const schoolsTable = document.querySelector('#schools-table tbody');
        schoolsTable.innerHTML = '';
        
        schools.forEach(school => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${school.name}</td>
                <td>${school.city}</td>
                <td>${school.students}</td>
                <td>${school.teachers}</td>
                <td><span class="badge ${getStatusBadgeClass(school.status)}">${getStatusText(school.status)}</span></td>
                <td>
                    <button class="btn btn-sm btn-outline-primary edit-school" data-school='${JSON.stringify(school)}'>
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
            schoolsTable.appendChild(row);
        });
        
        // Add event listeners to edit buttons
        document.querySelectorAll('.edit-school').forEach(btn => {
            btn.addEventListener('click', function() {
                const school = JSON.parse(this.getAttribute('data-school'));
                editSchool(school);
            });
        });
    }, 500);
}

function editSchool(school) {
    // In a real app, we would populate the form with actual school data
    document.getElementById('school-id').value = '123'; // Simulated ID
    document.getElementById('school-name').value = school.name;
    document.getElementById('school-address').value = '123 Rue de l\'École';
    document.getElementById('school-city').value = school.city;
    document.getElementById('school-phone').value = '01 23 45 67 89';
    document.getElementById('school-email').value = 'contact@ecole.com';
    document.getElementById('school-status').value = school.status;
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('school-modal'));
    modal.show();
}

function getStatusBadgeClass(status) {
    switch (status) {
        case 'active': return 'bg-success';
        case 'inactive': return 'bg-secondary';
        case 'maintenance': return 'bg-warning text-dark';
        default: return 'bg-light text-dark';
    }
}

function getStatusText(status) {
    switch (status) {
        case 'active': return 'Active';
        case 'inactive': return 'Inactive';
        case 'maintenance': return 'Maintenance';
        default: return status;
    }
}

function initCharts() {
    // Initialize schools status chart
    const ctx = document.createElement('canvas');
    document.getElementById('schools-status-chart').appendChild(ctx);
    
    window.schoolsStatusChart = new Chart(ctx.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: ['Active', 'Inactive', 'Maintenance'],
            datasets: [{
                data: [3, 1, 0],
                backgroundColor: [
                    '#2ecc71',
                    '#95a5a6',
                    '#f39c12'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function updateSchoolsStatusChart(schoolId) {
    // In a real app, this would fetch actual data
    if (schoolId === 'all') {
        window.schoolsStatusChart.data.datasets[0].data = [3, 1, 0];
    } else {
        window.schoolsStatusChart.data.datasets[0].data = [1, 0, 0];
    }
    window.schoolsStatusChart.update();
}