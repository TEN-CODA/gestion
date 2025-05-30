from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')
    avatar_url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    is_authenticated = db.Column(db.Boolean, default=True)
    is_anonymous = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

class Ecole(db.Model):
    __tablename__ = 'ecoles'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.Text)
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    directeur_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_creation = db.Column(db.Date)

class Eleve(db.Model):
    __tablename__ = 'eleves'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ecole_id = db.Column(db.Integer, db.ForeignKey('ecoles.id'))
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    date_naissance = db.Column(db.Date)
    adresse = db.Column(db.Text)
    telephone = db.Column(db.String(20))
    classe_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'))
    
    # Relations
    commentaires = db.relationship('Commentaire', backref='eleve', lazy=True)
    classe = db.relationship('Classe', backref='eleves')
    parent = db.relationship('Parent', backref='eleves')

class Parent(db.Model):
    __tablename__ = 'parents'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    adresse = db.Column(db.Text)
    profession = db.Column(db.String(100))

class Professeur(db.Model):
    __tablename__ = 'professeurs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ecole_id = db.Column(db.Integer, db.ForeignKey('ecoles.id'))
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    specialite = db.Column(db.String(100))
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    date_embauche = db.Column(db.Date)

class Classe(db.Model):
    __tablename__ = 'classes'
    
    id = db.Column(db.Integer, primary_key=True)
    ecole_id = db.Column(db.Integer, db.ForeignKey('ecoles.id'))
    nom = db.Column(db.String(50), nullable=False)
    niveau = db.Column(db.String(20))
    annee_scolaire = db.Column(db.String(9))
    professeur_principal_id = db.Column(db.Integer, db.ForeignKey('professeurs.id'))
    capacite = db.Column(db.Integer)

class Matiere(db.Model):
    __tablename__ = 'matieres'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    coefficient = db.Column(db.Integer, default=1)
    description = db.Column(db.Text)
    ecole_id = db.Column(db.Integer, db.ForeignKey('ecoles.id'))

class Cours(db.Model):
    __tablename__ = 'cours'
    
    id = db.Column(db.Integer, primary_key=True)
    classe_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    matiere_id = db.Column(db.Integer, db.ForeignKey('matieres.id'))
    professeur_id = db.Column(db.Integer, db.ForeignKey('professeurs.id'))
    jour_semaine = db.Column(db.String(10))
    heure_debut = db.Column(db.Time)
    heure_fin = db.Column(db.Time)
    salle = db.Column(db.String(50))
    
    # Relations
    classe = db.relationship('Classe', backref='cours')
    matiere = db.relationship('Matiere', backref='cours')
    professeur = db.relationship('Professeur', backref='cours')

class Evaluation(db.Model):
    __tablename__ = 'evaluations'
    
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date_evaluation = db.Column(db.Date, nullable=False)
    coefficient = db.Column(db.Float, default=1.0)
    type_evaluation = db.Column(db.String(50))  # ex: "Contrôle", "Devoir", "Examen"
    
    # Clés étrangères
    matiere_id = db.Column(db.Integer, db.ForeignKey('matieres.id'), nullable=False)
    classe_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    professeur_id = db.Column(db.Integer, db.ForeignKey('professeurs.id'), nullable=False)
    
    # Relations
    matiere = db.relationship('Matiere', backref='evaluations')
    classe = db.relationship('Classe', backref='evaluations')
    professeur = db.relationship('Professeur', backref='evaluations')
    notes = db.relationship('Note', back_populates='evaluation')

class Note(db.Model):
    __tablename__ = 'notes'
    
    id = db.Column(db.Integer, primary_key=True)
    evaluation_id = db.Column(db.Integer, db.ForeignKey('evaluations.id'))
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleves.id'))
    periode_id = db.Column(db.Integer, db.ForeignKey('periodes_scolaires.id'))
    valeur = db.Column(db.Float)
    commentaire = db.Column(db.Text)
    date_saisie = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    eleve = db.relationship('Eleve', backref='notes')
    evaluation = db.relationship('Evaluation', back_populates='notes')
    periode = db.relationship('PeriodeScolaire', back_populates='notes')

# Table d'association pour les élèves qui ont sauvegardé une annonce
eleves_annonces_sauvegardees = db.Table('eleves_annonces_sauvegardees',
    db.Column('eleve_id', db.Integer, db.ForeignKey('eleves.id'), primary_key=True),
    db.Column('annonce_id', db.Integer, db.ForeignKey('annonces.id'), primary_key=True)
)

# Table d'association pour les élèves inscrits à un événement
eleves_evenements_inscrits = db.Table('eleves_evenements_inscrits',
    db.Column('eleve_id', db.Integer, db.ForeignKey('eleves.id'), primary_key=True),
    db.Column('annonce_id', db.Integer, db.ForeignKey('annonces.id'), primary_key=True)
)

class Annonce(db.Model):
    __tablename__ = 'annonces'
    
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    date_creation = db.Column(db.DateTime, nullable=False, default=datetime.now)
    date_publication = db.Column(db.DateTime)
    date_evenement = db.Column(db.DateTime)
    lieu = db.Column(db.String(200))
    est_evenement = db.Column(db.Boolean, default=False)
    categorie = db.Column(db.String(50))
    type_destinataire = db.Column(db.String(50))
    priorite = db.Column(db.String(20))
    ecole_id = db.Column(db.Integer, db.ForeignKey('ecoles.id'))
    auteur_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relations
    commentaires = db.relationship('Commentaire', backref='annonce', lazy=True)
    eleves_sauvegardees = db.relationship('Eleve', 
                                        secondary='eleves_annonces_sauvegardees',
                                        backref=db.backref('annonces_sauvegardees', lazy='dynamic'))
    eleves_inscrits = db.relationship('Eleve',
                                    secondary='eleves_evenements_inscrits',
                                    backref=db.backref('evenements_inscrits', lazy='dynamic'))

class Commentaire(db.Model):
    __tablename__ = 'commentaires'
    
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.Text, nullable=False)
    date_creation = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    # Clés étrangères
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleves.id'), nullable=False)
    annonce_id = db.Column(db.Integer, db.ForeignKey('annonces.id'), nullable=False)

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    expediteur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    destinataire_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sujet = db.Column(db.String(255))
    contenu = db.Column(db.Text, nullable=False)
    date_envoi = db.Column(db.DateTime, default=datetime.utcnow)
    lu = db.Column(db.Boolean, default=False)
    type_message = db.Column(db.String(20), default='normal')
    
    # Relations
    expediteur = db.relationship('User', foreign_keys=[expediteur_id], backref='messages_envoyes')
    destinataire = db.relationship('User', foreign_keys=[destinataire_id], backref='messages_recus')

# Table d'association pour les membres des groupes
groupes_membres = db.Table('groupes_membres',
    db.Column('groupe_id', db.Integer, db.ForeignKey('groupes.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class Groupe(db.Model):
    __tablename__ = 'groupes'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    createur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relations
    createur = db.relationship('User', backref='groupes_crees')
    membres = db.relationship('User', secondary=groupes_membres, backref='groupes')

class PeriodeScolaire(db.Model):
    __tablename__ = 'periodes_scolaires'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)  # ex: "Premier Trimestre", "Deuxième Trimestre"
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date, nullable=False)
    annee_scolaire = db.Column(db.String(9), nullable=False)  # ex: "2023-2024"
    ecole_id = db.Column(db.Integer, db.ForeignKey('ecoles.id'), nullable=False)
    
    # Relations
    ecole = db.relationship('Ecole', backref=db.backref('periodes', lazy=True))
    notes = db.relationship('Note', back_populates='periode')
    
    def __repr__(self):
        return f'<PeriodeScolaire {self.nom} {self.annee_scolaire}>' 