username-- Création de la base de données
CREATE DATABASE IF NOT EXISTS gestion_ecole;
USE gestion_ecole;

-- 1. GESTION DES UTILISATEURS ET RÔLES
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    role ENUM('superadmin', 'admin_ecole', 'professeur', 'parent', 'eleve') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    avatar_url VARCHAR(255)
);

CREATE TABLE Ecole (
    ecole_id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    adresse TEXT,
    telephone VARCHAR(20),
    email VARCHAR(100),
    directeur_id INT,
    date_creation DATE,
    FOREIGN KEY (directeur_id) REFERENCES Users(user_id)
);

-- 2. GESTION DES ÉLÈVES ET PARENTS
CREATE TABLE Parents (
    parent_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    telephone VARCHAR(20),
    email VARCHAR(100),
    adresse TEXT,
    profession VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Classes (
    classe_id INT PRIMARY KEY AUTO_INCREMENT,
    ecole_id INT,
    nom VARCHAR(50) NOT NULL,
    niveau VARCHAR(20),
    annee_scolaire VARCHAR(9),
    professeur_principal_id INT,
    capacite INT,
    FOREIGN KEY (ecole_id) REFERENCES Ecole(ecole_id)
);

CREATE TABLE Eleves (
    eleve_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    ecole_id INT,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    date_naissance DATE,
    adresse TEXT,
    telephone VARCHAR(20),
    classe_id INT,
    parent_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (ecole_id) REFERENCES Ecole(ecole_id),
    FOREIGN KEY (classe_id) REFERENCES Classes(classe_id),
    FOREIGN KEY (parent_id) REFERENCES Parents(parent_id)
);

-- 3. GESTION DES PROFESSEURS ET CLASSES
CREATE TABLE Professeurs (
    professeur_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    ecole_id INT,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    specialite VARCHAR(100),
    telephone VARCHAR(20),
    email VARCHAR(100),
    date_embauche DATE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (ecole_id) REFERENCES Ecole(ecole_id)
);

-- 4. GESTION DES COURS ET ÉVALUATIONS
CREATE TABLE Matieres (
    matiere_id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    coefficient INT DEFAULT 1,
    description TEXT
);

CREATE TABLE Cours (
    cours_id INT PRIMARY KEY AUTO_INCREMENT,
    classe_id INT,
    matiere_id INT,
    professeur_id INT,
    jour_semaine ENUM('Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'),
    heure_debut TIME,
    heure_fin TIME,
    salle VARCHAR(50),
    FOREIGN KEY (classe_id) REFERENCES Classes(classe_id),
    FOREIGN KEY (matiere_id) REFERENCES Matieres(matiere_id),
    FOREIGN KEY (professeur_id) REFERENCES Professeurs(professeur_id)
);

CREATE TABLE Evaluations (
    evaluation_id INT PRIMARY KEY AUTO_INCREMENT,
    cours_id INT,
    type_evaluation ENUM('Contrôle', 'Devoir', 'Examen', 'Projet'),
    date_evaluation DATE,
    coefficient INT DEFAULT 1,
    description TEXT,
    FOREIGN KEY (cours_id) REFERENCES Cours(cours_id)
);

CREATE TABLE Notes (
    note_id INT PRIMARY KEY AUTO_INCREMENT,
    evaluation_id INT,
    eleve_id INT,
    valeur DECIMAL(4,2),
    commentaire TEXT,
    date_saisie TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (evaluation_id) REFERENCES Evaluations(evaluation_id),
    FOREIGN KEY (eleve_id) REFERENCES Eleves(eleve_id)
);

-- 5. COMMUNICATION ET ANNONCES
CREATE TABLE Messages (
    message_id INT PRIMARY KEY AUTO_INCREMENT,
    expediteur_id INT,
    destinataire_id INT,
    sujet VARCHAR(255),
    contenu TEXT,
    date_envoi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lu BOOLEAN DEFAULT FALSE,
    type_message ENUM('normal', 'urgent', 'systeme'),
    FOREIGN KEY (expediteur_id) REFERENCES Users(user_id),
    FOREIGN KEY (destinataire_id) REFERENCES Users(user_id)
);

CREATE TABLE Annonces (
    annonce_id INT PRIMARY KEY AUTO_INCREMENT,
    ecole_id INT,
    titre VARCHAR(255) NOT NULL,
    contenu TEXT,
    date_publication TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_expiration TIMESTAMP,
    auteur_id INT,
    type_destinataire ENUM('tous', 'professeurs', 'parents', 'eleves', 'classes_specifiques'),
    priorite ENUM('normale', 'importante', 'urgente'),
    FOREIGN KEY (ecole_id) REFERENCES Ecole(ecole_id),
    FOREIGN KEY (auteur_id) REFERENCES Users(user_id)
);

-- 6. GESTION ADMINISTRATIVE
CREATE TABLE Parametres_Ecole (
    parametre_id INT PRIMARY KEY AUTO_INCREMENT,
    ecole_id INT,
    nom_etablissement VARCHAR(100),
    adresse TEXT,
    telephone VARCHAR(20),
    email VARCHAR(100),
    site_web VARCHAR(255),
    logo_url VARCHAR(255),
    annee_scolaire_courante VARCHAR(9),
    date_debut_annee DATE,
    date_fin_annee DATE,
    FOREIGN KEY (ecole_id) REFERENCES Ecole(ecole_id)
);

CREATE TABLE Convocations (
    convocation_id INT PRIMARY KEY AUTO_INCREMENT,
    ecole_id INT,
    titre VARCHAR(255) NOT NULL,
    description TEXT,
    date_convocation DATETIME,
    type_convocation ENUM('conseil_classe', 'reunion_parents', 'reunion_profs', 'autre'),
    statut ENUM('planifiee', 'en_cours', 'terminee', 'annulee'),
    FOREIGN KEY (ecole_id) REFERENCES Ecole(ecole_id)
);

-- 7. SUIVI ET PERFORMANCES
CREATE TABLE Performances_Classe (
    performance_id INT PRIMARY KEY AUTO_INCREMENT,
    classe_id INT,
    matiere_id INT,
    periode VARCHAR(20),
    moyenne_classe DECIMAL(4,2),
    taux_reussite DECIMAL(5,2),
    meilleure_note DECIMAL(4,2),
    pire_note DECIMAL(4,2),
    date_calcul TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (classe_id) REFERENCES Classes(classe_id),
    FOREIGN KEY (matiere_id) REFERENCES Matieres(matiere_id)
);

CREATE TABLE Suivi_Professeur (
    suivi_id INT PRIMARY KEY AUTO_INCREMENT,
    professeur_id INT,
    date_evaluation DATE,
    type_evaluation ENUM('annuelle', 'trimestrielle', 'exceptionnelle'),
    note_evaluation DECIMAL(4,2),
    commentaires TEXT,
    evaluateur_id INT,
    FOREIGN KEY (professeur_id) REFERENCES Professeurs(professeur_id),
    FOREIGN KEY (evaluateur_id) REFERENCES Users(user_id)
);

-- 8. SUPPORT ET DOCUMENTATION
CREATE TABLE Support_Tickets (
    ticket_id INT PRIMARY KEY AUTO_INCREMENT,
    ecole_id INT,
    expediteur_id INT,
    sujet VARCHAR(255),
    description TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    statut ENUM('ouvert', 'en_cours', 'resolu', 'ferme'),
    priorite ENUM('basse', 'moyenne', 'haute', 'urgente'),
    categorie VARCHAR(50),
    FOREIGN KEY (ecole_id) REFERENCES Ecole(ecole_id),
    FOREIGN KEY (expediteur_id) REFERENCES Users(user_id)
);

CREATE TABLE Documents (
    document_id INT PRIMARY KEY AUTO_INCREMENT,
    titre VARCHAR(255) NOT NULL,
    type_document ENUM('bulletin', 'certificat', 'attestation', 'autre'),
    url_fichier VARCHAR(255),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    eleve_id INT,
    classe_id INT,
    FOREIGN KEY (eleve_id) REFERENCES Eleves(eleve_id),
    FOREIGN KEY (classe_id) REFERENCES Classes(classe_id)
); 