from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, time, timedelta
from models import db, User, Ecole, Eleve, Parent, Professeur, Classe, Matiere, Cours, Evaluation, Note, Annonce, Commentaire, Message, Groupe, groupes_membres, PeriodeScolaire
from config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

# Initialisation de la base de données
db.init_app(app)
migrate = Migrate(app, db)

# Configuration de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route par défaut
@app.route('/')
def home():
    return redirect(url_for('login'))

# Routes d'authentification
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            if user.role == 'eleve':
                return redirect(url_for('eleve_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        flash('Nom d\'utilisateur ou mot de passe incorrect')
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        if User.query.filter_by(username=username).first():
            flash('Ce nom d\'utilisateur existe déjà')
            return redirect(url_for('register'))
            
        if User.query.filter_by(email=email).first():
            flash('Cet email est déjà utilisé')
            return redirect(url_for('register'))
            
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Inscription réussie ! Vous pouvez maintenant vous connecter.')
        return redirect(url_for('login'))
    return render_template('auth/register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Routes protégées
@app.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
        
    if current_user.role == 'superadmin':
        return render_template('superadmin/index.html')
    elif current_user.role == 'admin':
        return render_template('admEcole/index.html')
    elif current_user.role == 'professeur':
        return render_template('professeurs/index.html')
    elif current_user.role == 'parent':
        return render_template('parents/html/index.html')
    elif current_user.role == 'eleve':
        return render_template('eleves/index.html')
    else:
        flash('Rôle non reconnu')
        return redirect(url_for('login'))

#index des professeurs
@app.route("/professeurs")
def professeurs_index():
    print(request.args)
    return render_template("professeurs/index.html")

#controles des professeurs
@app.route("/professeurs/controls")
def controls():
  return render_template("professeurs/controles.html")  

#cours des professeurs
@app.route("/professeurs/cours")
def cours():
  return render_template("professeurs/cours.html")  

#eleves des professeurs
@app.route("/professeurs/eleves")
def eleves():
  return render_template("professeurs/eleves.html")  

#infosEleves des professeurs
@app.route("/professeurs/infosEleve")
def infosEleve():
  return render_template("professeurs/infosEleve.html")  

#messageries des professeurs
@app.route("/professeurs/messagerie")
def messagerie():
  return render_template("professeurs/messagerie.html")  

#saisie note des professeurs
@app.route("/professeurs/notes")
def saisieNotes():
  return render_template("professeurs/saisie-notes.html")  

#index des parents
@app.route("/parents")
def indexParent():
    return render_template("parents/html/index.html")

#enfants des parents
@app.route("/parents/enfants")
def enfantParent():
    return render_template("parents/html/enfants.html")

#calendrier des parents
@app.route("/parents/calendrier")
def calendrierParent():
    return render_template("parents/html/calendier.html")

#enfantX des parents
@app.route("/parents/enfantX")
def enfantXParent():
    return render_template("parents/html/enfantX.html")

#horaire des parents
@app.route("/parents/horaire")
def horaireParent():
    return render_template("parents/html/horaire.html")

#messagerie des parents
@app.route("/parents/messagerie")
def messagerieParent():
    return render_template("parents/html/messagerie.html")

#notifications des parents
@app.route("/parents/notifications")
def notificationsParent():
    return render_template("parents/html/notifications.html")

#paiements des parents
@app.route("/parents/paiements")
def paiementsParent():
    return render_template("parents/html/paiements.html")

#param des parents
@app.route("/parents/parametre")
def parametreParent():
    return render_template("parents/html/param.html")

#performance des parents
@app.route("/parents/performance")
def performanceParent():
    return render_template("parents/html/performance.html")

#index ecoles
@app.route("/ecole")
def indexEcole():
    # Pour l'instant, on prend la première école (à adapter selon le contexte utilisateur)
    ecole = Ecole.query.first()
    if not ecole:
        return render_template("admEcole/index.html", nb_eleves=0, nb_profs=0, nb_classes=0, nb_parents=0, taux_presence=0, nouvelles_demandes=0)
    nb_eleves = Eleve.query.filter_by(ecole_id=ecole.id).count()
    nb_profs = Professeur.query.filter_by(ecole_id=ecole.id).count()
    nb_classes = Classe.query.filter_by(ecole_id=ecole.id).count()
    nb_parents = Parent.query.count()  # À affiner si besoin par école
    taux_presence = 98  # À calculer dynamiquement si la donnée existe
    nouvelles_demandes = 24  # À calculer dynamiquement si la donnée existe
    return render_template("admEcole/index.html",
        nb_eleves=nb_eleves,
        nb_profs=nb_profs,
        nb_classes=nb_classes,
        nb_parents=nb_parents,
        taux_presence=taux_presence,
        nouvelles_demandes=nouvelles_demandes
    )

#agenda ecoles
@app.route("/ecole/agenda")
def agendaEcole():
  return render_template("admEcole/agenda.html")  

#ajouter eleve ecoles
@app.route("/ecole/ajouterEleve", methods=['GET', 'POST'])
@login_required
def ajouterEleveEcole():
    print("Début de la fonction ajouterEleveEcole")
    if current_user.role != 'admin':
        print("Accès non autorisé - Rôle:", current_user.role)
        flash('Accès non autorisé')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        try:
            print("Méthode POST détectée")
            # Récupérer les données du formulaire
            nom = request.form.get('nom')
            prenom = request.form.get('prenom')
            date_naissance = request.form.get('date_naissance')
            classe_id = request.form.get('classe_id')
            parent_nom = request.form.get('parent_nom')
            parent_prenom = request.form.get('parent_prenom')
            parent_email = request.form.get('parent_email')
            parent_telephone = request.form.get('parent_telephone')
            
            print(f"Données reçues - Nom: {nom}, Prénom: {prenom}, Classe: {classe_id}")
            
            # Validation des données requises
            if not all([nom, prenom, classe_id]):
                print("Données manquantes")
                flash('Veuillez remplir tous les champs obligatoires')
                return redirect(url_for('ajouterEleveEcole'))
            
            # Récupérer l'école
            ecole = Ecole.query.first()
            if not ecole:
                print("Aucune école trouvée")
                flash('Aucune école trouvée')
                return redirect(url_for('ajouterEleveEcole'))
            
            print(f"École trouvée: {ecole.nom}")
            
            # Vérifier si la classe existe
            classe = Classe.query.get(classe_id)
            if not classe:
                print(f"Classe non trouvée: {classe_id}")
                flash('Classe non trouvée')
                return redirect(url_for('ajouterEleveEcole'))
            
            print(f"Classe trouvée: {classe.nom}")

            # Créer le compte utilisateur pour l'élève
            username = f"{prenom.lower()}.{nom.lower()}"
            email = f"{username}@{ecole.nom.lower().replace(' ', '')}.com"
            password = f"{prenom}{nom}123"  # Mot de passe temporaire
            
            print(f"Création du compte utilisateur - Username: {username}, Email: {email}")
            
            # Vérifier si le nom d'utilisateur existe déjà
            if User.query.filter_by(username=username).first():
                username = f"{username}{datetime.now().strftime('%Y%m%d')}"
                print(f"Nom d'utilisateur modifié: {username}")
            
            # Créer l'utilisateur
            user = User(
                username=username,
                email=email,
                role='eleve'
            )
            user.set_password(password)
            db.session.add(user)
            db.session.flush()  # Pour obtenir l'ID de l'utilisateur
            
            print(f"Compte utilisateur créé avec l'ID: {user.id}")
            
            # Créer le parent si les informations sont fournies
            parent = None
            if parent_nom:  # On vérifie seulement si le nom du parent est fourni
                print("Création du compte parent")
                # Créer le compte utilisateur pour le parent
                parent_username = f"parent.{prenom.lower()}.{nom.lower()}"
                if User.query.filter_by(username=parent_username).first():
                    parent_username = f"{parent_username}{datetime.now().strftime('%Y%m%d')}"
                
                # Si l'email n'est pas fourni, on en génère un
                parent_email = parent_email or f"{parent_username}@{ecole.nom.lower().replace(' ', '')}.com"
                
                parent_user = User(
                    username=parent_username,
                    email=parent_email,
                    role='parent'
                )
                parent_user.set_password(f"parent{parent_nom}123")  # Mot de passe temporaire
                db.session.add(parent_user)
                db.session.flush()
                
                print(f"Compte parent créé avec l'ID: {parent_user.id}")
                
                parent = Parent(
                    user_id=parent_user.id,
                    nom=parent_nom,
                    prenom=parent_prenom,
                    email=parent_email,
                    telephone=parent_telephone
                )
                db.session.add(parent)
                db.session.flush()
                print(f"Enregistrement parent créé avec l'ID: {parent.id}")
            
            # Créer l'élève
            print("Création de l'enregistrement élève")
            nouvel_eleve = Eleve(
                user_id=user.id,
                nom=nom,
                prenom=prenom,
                date_naissance=datetime.strptime(date_naissance, '%Y-%m-%d') if date_naissance else None,
                classe_id=classe_id,
                parent_id=parent.id if parent else None,
                ecole_id=ecole.id
            )
            
            db.session.add(nouvel_eleve)
            db.session.commit()
            print(f"Élève créé avec succès - ID: {nouvel_eleve.id}")
            
            # Préparer le message de succès avec les informations de connexion
            success_message = f'Élève {prenom} {nom} a été ajouté avec succès !\n'
            success_message += f'Identifiants de connexion :\n'
            success_message += f'Nom d\'utilisateur : {username}\n'
            success_message += f'Mot de passe : {password}'
            if parent:
                success_message += f'\n\nIdentifiants du parent :\n'
                success_message += f'Nom d\'utilisateur : {parent_username}\n'
                success_message += f'Mot de passe : parent{parent_nom}123'
            
            flash(success_message)
            return redirect(url_for('elevesAdmEcole'))
            
        except Exception as e:
            db.session.rollback()
            print(f"ERREUR lors de l'ajout de l'élève: {str(e)}")
            print(f"Type d'erreur: {type(e)}")
            import traceback
            print(f"Traceback complet:\n{traceback.format_exc()}")
            flash(f'Erreur lors de l\'ajout de l\'élève: {str(e)}')
            return redirect(url_for('ajouterEleveEcole'))
    
    # Pour GET, récupérer les classes disponibles
    print("Méthode GET - Récupération des classes")
    ecole = Ecole.query.first()
    classes = Classe.query.filter_by(ecole_id=ecole.id).all() if ecole else []
    print(f"Nombre de classes trouvées: {len(classes)}")
    return render_template("admEcole/ajouterEleve.html", classes=classes)

@app.route("/ecole/ajouterProf", methods=['GET', 'POST'])
def ajouterProfEcole():
    if request.method == 'POST':
        if current_user.role != 'admin':
            flash('Accès non autorisé', 'error')
            return redirect(url_for('indexEcole'))
            
        try:
            # Récupérer les données du formulaire
            nom = request.form.get('nom')
            prenom = request.form.get('prenom')
            email = request.form.get('email')
            telephone = request.form.get('telephone')
            specialite = request.form.get('specialite')
            
            print(f"Données reçues - Nom: {nom}, Prénom: {prenom}, Email: {email}")
            
            # Récupérer l'école
            ecole = Ecole.query.first()
            if not ecole:
                flash('Aucune école trouvée', 'error')
                return redirect(url_for('indexEcole'))
            
            # Créer le professeur
            professeur = Professeur(
                nom=nom,
                prenom=prenom,
                email=email,
                telephone=telephone,
                specialite=specialite,
                ecole_id=ecole.id
            )
            
            db.session.add(professeur)
            db.session.flush()  # Pour obtenir l'ID du professeur
            
            # Récupérer les matières et classes sélectionnées
            matieres_ids = request.form.getlist('matieres')
            classes_ids = request.form.getlist('classes')
            
            print(f"Matières sélectionnées: {matieres_ids}")
            print(f"Classes sélectionnées: {classes_ids}")
            
            # Vérifier que les IDs sont valides
            for matiere_id in matieres_ids:
                matiere = Matiere.query.get(int(matiere_id))
                if not matiere:
                    raise ValueError(f"Matière avec l'ID {matiere_id} non trouvée")
            
            for classe_id in classes_ids:
                classe = Classe.query.get(int(classe_id))
                if not classe:
                    raise ValueError(f"Classe avec l'ID {classe_id} non trouvée")
            
            # Créer les cours pour chaque combinaison matière/classe
            for matiere_id in matieres_ids:
                for classe_id in classes_ids:
                    cours = Cours(
                        professeur_id=professeur.id,
                        matiere_id=int(matiere_id),
                        classe_id=int(classe_id)
                    )
                    db.session.add(cours)
            
            db.session.commit()
            flash('Professeur ajouté avec succès', 'success')
            return redirect(url_for('professeursEcole'))
            
        except ValueError as e:
            db.session.rollback()
            print(f"Erreur de validation: {str(e)}")
            flash(f'Erreur de validation: {str(e)}', 'error')
            return redirect(url_for('ajouterProfEcole'))
        except Exception as e:
            db.session.rollback()
            print(f"Erreur inattendue: {str(e)}")
            flash(f'Une erreur est survenue: {str(e)}', 'error')
            return redirect(url_for('ajouterProfEcole'))
        
    # Pour GET, récupérer les matières et classes de l'école
    ecole = Ecole.query.first()
    if not ecole:
        flash('Aucune école trouvée', 'error')
        return redirect(url_for('indexEcole'))
        
    matieres = Matiere.query.filter_by(ecole_id=ecole.id).all()
    classes = Classe.query.filter_by(ecole_id=ecole.id).all()
    
    return render_template("admEcole/ajouterProf.html", matieres=matieres, classes=classes)

#contacter super adm ecoles
@app.route("/ecole/contacteSuperAdm")
def contacteSuperAdmEcole():
  return render_template("admEcole/contacteSuperAdmin.html")  

#eleves ecoles
@app.route("/ecole/eleves")
def elevesAdmEcole():
    # Récupérer l'école de l'utilisateur connecté
    ecole = Ecole.query.first()  # À adapter selon le contexte utilisateur
    if not ecole:
        return render_template("admEcole/eleves.html", eleves=[])
    
    # Récupérer tous les élèves de l'école
    eleves = Eleve.query.filter_by(ecole_id=ecole.id).all()
    
    # Récupérer les classes pour l'affichage
    classes = Classe.query.filter_by(ecole_id=ecole.id).all()
    
    return render_template("admEcole/eleves.html", eleves=eleves, classes=classes)

@app.route("/ecole/eleveX/<int:eleve_id>")
@login_required
def eleveXAdmEcole(eleve_id):
    if current_user.role != 'admin':
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))
    
    try:
        # Récupérer l'élève
        eleve = Eleve.query.get_or_404(eleve_id)
        
        # Récupérer l'école
        ecole = Ecole.query.first()
        if not ecole:
            flash('Aucune école trouvée', 'error')
            return redirect(url_for('elevesAdmEcole'))
        
        # Vérifier que l'élève appartient à l'école
        if eleve.ecole_id != ecole.id:
            flash('Accès non autorisé', 'error')
            return redirect(url_for('elevesAdmEcole'))
        
        # Récupérer les informations supplémentaires si nécessaire
        # Par exemple, les notes, les absences, etc.
        
        return render_template("admEcole/eleveX.html", 
                             eleve=eleve,
                             classe=eleve.classe,
                             parent=eleve.parent)
                             
    except Exception as e:
        print(f"ERREUR lors de l'affichage des détails de l'élève: {str(e)}")
        flash(f'Une erreur est survenue : {str(e)}', 'error')
        return redirect(url_for('elevesAdmEcole'))

#messagerie ecoles
@app.route("/ecole/messagerie")
def messagerieEcole():
  return render_template("admEcole/messagerie.html")  

@app.route("/ecole/notesEtBulletin")
@login_required
def notesEtBulletinEcole():
    return render_template('admEcole/notesEtBulletin.html')

#Performances ecoles
@app.route("/ecole/Performances")
def PerformancesEcole():
  return render_template("admEcole/Performances.html")  

#Performances ecoles
@app.route("/ecole/professeurs")
@login_required
def professeursEcole():
    if current_user.role != 'admin':
        flash('Accès non autorisé', 'error')
        return redirect(url_for('indexEcole'))
        
    # Récupérer l'école
    ecole = Ecole.query.first()
    if not ecole:
        flash('Aucune école trouvée', 'error')
        return redirect(url_for('indexEcole'))
    
    # Récupérer tous les professeurs de l'école
    professeurs = Professeur.query.filter_by(ecole_id=ecole.id).all()
    
    # Récupérer toutes les classes de l'école
    classes = Classe.query.filter_by(ecole_id=ecole.id).all()
    
    return render_template("admEcole/professeurs.html", professeurs=professeurs, classes=classes)

#Profil prof ecoles
@app.route("/ecole/profilProf")
def profilProfEcole():
  return render_template("admEcole/profilProf.html")  

#index superAdmin
@app.route("/superAdmin")
def superadmin_index():
  return render_template("superAdmin/index.html")  

#Ajout ecole superAdmin
@app.route("/superAdmin/ajouterEcole")
def ajoutEcoleSuperAd():
  return render_template("superAdmin/ajouter-ecole.html")  

#Ajout ticket superAdmin
@app.route("/superAdmin/ajouterTicket")
def ajoutTicketSuperAd():
  return render_template("superAdmin/ajouter-ticket.html")  

#Ajout utilisateur superAdmin
@app.route("/superAdmin/ajouterUtilisateur")
def ajoutUtilisateurSuperAd():
  return render_template("superAdmin/ajouter-utilisateur.html")  

#Ecoles superAdmin
@app.route("/superAdmin/ecoles")
def ecolesSuperAd():
  return render_template("superAdmin/ecoles.html")  

#Generer rapport superAdmin
@app.route("/superAdmin/genererRapport")
def genererRapportSuperAd():
  return render_template("superAdmin/generer-rapport.html")  

#messagerie superAdmin
@app.route("/superAdmin/messagerie")
def messagerieSuperAd():
  return render_template("superAdmin/messagerie.html")  

#parametres superAdmin
@app.route("/superAdmin/parametres")
def parametresSuperAd():
  return render_template("superAdmin/parametres.html")  

#rapports superAdmin
@app.route("/superAdmin/rapports")
def rapportsSuperAd():
  return render_template("superAdmin/rapports.html")  

#support superAdmin
@app.route("/superAdmin/support")
def supportSuperAd():
  return render_template("superAdmin/support.html")  

#utilisateurs superAdmin
@app.route("/superAdmin/users")
def usersSuperAd():
  return render_template("superAdmin/utilisateurs.html")  

# Routes pour l'administration de l'école
@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Accès non autorisé')
        return redirect(url_for('dashboard'))
    return render_template('admEcole/index.html')

# Gestion des classes
@app.route('/admin/classes')
@login_required
def admin_classes():
    if current_user.role != 'admin':
        flash('Accès non autorisé')
        return redirect(url_for('dashboard'))
    classes = Classe.query.filter_by(ecole_id=current_user.ecole_id).all()
    professeurs = Professeur.query.filter_by(ecole_id=current_user.ecole_id).all()
    return render_template('admEcole/classes.html', classes=classes, professeurs=professeurs)

@app.route('/admin/classes/ajouter', methods=['POST'])
@login_required
def ajouter_classe():
    if current_user.role != 'admin':
        return jsonify({'error': 'Accès non autorisé'}), 403
    
    nom = request.form.get('nom')
    niveau = request.form.get('niveau')
    annee_scolaire = request.form.get('annee_scolaire')
    professeur_principal_id = request.form.get('professeur_principal_id')
    capacite = request.form.get('capacite')
    
    nouvelle_classe = Classe(
        ecole_id=current_user.ecole_id,
        nom=nom,
        niveau=niveau,
        annee_scolaire=annee_scolaire,
        professeur_principal_id=professeur_principal_id,
        capacite=capacite
    )
    
    db.session.add(nouvelle_classe)
    db.session.commit()
    flash('Classe ajoutée avec succès')
    return redirect(url_for('admin_classes'))

# Gestion des élèves
@app.route('/admin/eleves')
@login_required
def admin_eleves():
    return render_template('admin/eleves.html')

@app.route('/admin/eleve/<int:eleve_id>')
@login_required
def admin_eleve_details(eleve_id):
    return render_template('admin/eleveX.html')

# Gestion des professeurs
@app.route('/admin/professeurs')
@login_required
def admin_professeurs():
    return render_template('admin/professeurs.html')

@app.route('/admin/professeur/<int:prof_id>')
@login_required
def admin_professeur_details(prof_id):
    return render_template('admin/profilProf.html')

@app.route('/admin/ajouter-eleve')
@login_required
def admin_ajouter_eleve():
    return render_template('admin/ajouterEleve.html')

@app.route('/admin/messagerie')
@login_required
def admin_messagerie():
    return render_template('admin/messagerie.html')

@app.route('/admin/notes-bulletins')
@login_required
def admin_notes_bulletins():
    return render_template('admin/notesEtBulletin.html')

@app.route('/admin/performances')
@login_required
def admin_performances():
    return render_template('admin/performances.html')

@app.route('/admin/contact-superadmin')
@login_required
def admin_contact_superadmin():
    return render_template('admin/contacteSuperAdmin.html')

# Routes pour les parents
@app.route('/parent')
@login_required
def parent_dashboard():
    return render_template('parent/index.html')

@app.route('/parent/enfants')
@login_required
def parent_enfants():
    return render_template('parent/enfants.html')

@app.route('/parent/enfant/<int:eleve_id>')
@login_required
def parent_eleve_details(eleve_id):
    return render_template('parent/enfantX.html')

@app.route('/parent/calendrier')
@login_required
def parent_calendrier():
    return render_template('parent/calendier.html')

@app.route('/parent/messagerie')
@login_required
def parent_messagerie():
    return render_template('parent/messagerie.html')

@app.route('/parent/notifications')
@login_required
def parent_notifications():
    return render_template('parent/notifications.html')

@app.route('/parent/paiements')
@login_required
def parent_paiements():
    return render_template('parent/paiements.html')

@app.route('/parent/parametres')
@login_required
def parent_parametres():
    return render_template('parent/param.html')

@app.route('/parent/performance')
@login_required
def parent_performance():
    return render_template('parent/performance.html')

# Routes pour le super administrateur
@app.route('/superadmin')
@login_required
def superadmin_dashboard():
    if current_user.role != 'superadmin':
        flash('Accès non autorisé')
        return redirect(url_for('dashboard'))
    
    # Statistiques pour le tableau de bord
    total_ecoles = Ecole.query.count()
    total_users = User.query.count()
    total_professeurs = Professeur.query.count()
    total_eleves = Eleve.query.count()
    
    # Dernières activités (dernières connexions)
    recent_users = User.query.order_by(User.last_login.desc()).limit(5).all()
    
    # Statistiques des écoles
    ecoles_stats = []
    for ecole in Ecole.query.all():
        stats = {
            'nom': ecole.nom,
            'total_eleves': Eleve.query.filter_by(ecole_id=ecole.id).count(),
            'total_professeurs': Professeur.query.filter_by(ecole_id=ecole.id).count(),
            'total_classes': Classe.query.filter_by(ecole_id=ecole.id).count()
        }
        ecoles_stats.append(stats)
    
    # Statistiques des utilisateurs par rôle
    users_by_role = {
        'superadmin': User.query.filter_by(role='superadmin').count(),
        'admin': User.query.filter_by(role='admin').count(),
        'professeur': User.query.filter_by(role='professeur').count(),
        'eleve': User.query.filter_by(role='eleve').count(),
        'parent': User.query.filter_by(role='parent').count()
    }
    
    # Écoles récemment ajoutées
    recent_ecoles = Ecole.query.order_by(Ecole.date_creation.desc()).limit(2).all()
    
    return render_template('superadmin/index.html',
                         total_ecoles=total_ecoles,
                         total_users=total_users,
                         total_professeurs=total_professeurs,
                         total_eleves=total_eleves,
                         recent_users=recent_users,
                         ecoles_stats=ecoles_stats,
                         users_by_role=users_by_role,
                         recent_ecoles=recent_ecoles)

@app.route('/superadmin/ecoles')
@login_required
def superadmin_ecoles():
    if current_user.role != 'superadmin':
        flash('Accès non autorisé')
        return redirect(url_for('dashboard'))
    ecoles = Ecole.query.all()
    return render_template('superadmin/ecoles.html', ecoles=ecoles)

@app.route('/superadmin/ecoles/ajouter', methods=['GET', 'POST'])
@login_required
def superadmin_ajouter_ecole():
    if current_user.role != 'superadmin':
        flash('Accès non autorisé')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        nom = request.form.get('nom')
        adresse = request.form.get('adresse')
        telephone = request.form.get('telephone')
        email = request.form.get('email')
        
        nouvelle_ecole = Ecole(
            nom=nom,
            adresse=adresse,
            telephone=telephone,
            email=email,
            date_creation=datetime.utcnow().date()
        )
        
        db.session.add(nouvelle_ecole)
        db.session.commit()
        flash('École ajoutée avec succès')
        return redirect(url_for('superadmin_ecoles'))
    
    return render_template('superadmin/ajouter-ecole.html')

@app.route('/superadmin/utilisateurs')
@login_required
def superadmin_utilisateurs():
    if current_user.role != 'superadmin':
        flash('Accès non autorisé')
        return redirect(url_for('dashboard'))
    users = User.query.all()
    return render_template('superadmin/utilisateurs.html', users=users)

@app.route('/superadmin/utilisateurs/ajouter', methods=['GET', 'POST'])
@login_required
def superadmin_ajouter_utilisateur():
    if current_user.role != 'superadmin':
        flash('Accès non autorisé')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        ecole_id = request.form.get('ecole_id')
        
        if User.query.filter_by(username=username).first():
            flash('Ce nom d\'utilisateur existe déjà')
            return redirect(url_for('superadmin_ajouter_utilisateur'))
            
        if User.query.filter_by(email=email).first():
            flash('Cet email est déjà utilisé')
            return redirect(url_for('superadmin_ajouter_utilisateur'))
            
        user = User(username=username, email=email, role=role, ecole_id=ecole_id)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Utilisateur ajouté avec succès')
        return redirect(url_for('superadmin_utilisateurs'))
        
    ecoles = Ecole.query.all()
    return render_template('superadmin/ajouter-utilisateur.html', ecoles=ecoles)

@app.route('/superadmin/utilisateurs/<int:user_id>', methods=['GET', 'POST'])
@login_required
def superadmin_utilisateur_details(user_id):
    if current_user.role != 'superadmin':
        flash('Accès non autorisé')
        return redirect(url_for('dashboard'))
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.role = request.form.get('role')
        user.ecole_id = request.form.get('ecole_id')
        user.is_active = request.form.get('status') == 'active'
        
        password = request.form.get('password')
        if password:
            user.set_password(password)
            
        db.session.commit()
        flash('Utilisateur modifié avec succès')
        return redirect(url_for('superadmin_utilisateurs'))
        
    ecoles = Ecole.query.all()
    return render_template('superadmin/utilisateur-details.html', user=user, ecoles=ecoles)

@app.route('/superadmin/utilisateurs/<int:user_id>/supprimer', methods=['POST'])
@login_required
def superadmin_supprimer_utilisateur(user_id):
    if current_user.role != 'superadmin':
        flash('Accès non autorisé')
        return redirect(url_for('dashboard'))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Utilisateur supprimé avec succès')
    return redirect(url_for('superadmin_utilisateurs'))

#emploi du temps des professeurs
@app.route("/professeurs/emploi-du-temps")
def professeur_emploi_du_temps():
    # Données d'exemple pour l'emploi du temps
    horaires = [
        {'heure': '8h00-9h00'},
        {'heure': '9h00-10h00'},
        {'heure': '10h00-11h00'},
        {'heure': '11h00-12h00'},
        {'heure': '14h00-15h00'},
        {'heure': '15h00-16h00'},
        {'heure': '16h00-17h00'}
    ]

    # Données d'exemple pour l'emploi du temps
    emploi_du_temps = {
        'lundi': {
            '8h00-9h00': {'matiere': 'Mathématiques', 'classe': '6ème A', 'salle': 'Salle 101'},
            '9h00-10h00': {'matiere': 'Mathématiques', 'classe': '5ème B', 'salle': 'Salle 102'},
            '14h00-15h00': {'matiere': 'Mathématiques', 'classe': '4ème A', 'salle': 'Salle 103'}
        },
        'mardi': {
            '10h00-11h00': {'matiere': 'Mathématiques', 'classe': '6ème B', 'salle': 'Salle 101'},
            '11h00-12h00': {'matiere': 'Mathématiques', 'classe': '5ème A', 'salle': 'Salle 102'}
        },
        'mercredi': {
            '8h00-9h00': {'matiere': 'Mathématiques', 'classe': '4ème B', 'salle': 'Salle 103'},
            '9h00-10h00': {'matiere': 'Mathématiques', 'classe': '6ème A', 'salle': 'Salle 101'}
        },
        'jeudi': {
            '14h00-15h00': {'matiere': 'Mathématiques', 'classe': '5ème B', 'salle': 'Salle 102'},
            '15h00-16h00': {'matiere': 'Mathématiques', 'classe': '6ème B', 'salle': 'Salle 101'}
        },
        'vendredi': {
            '8h00-9h00': {'matiere': 'Mathématiques', 'classe': '4ème A', 'salle': 'Salle 103'},
            '9h00-10h00': {'matiere': 'Mathématiques', 'classe': '5ème A', 'salle': 'Salle 102'}
        }
    }

    # Données d'exemple pour les activités
    activites = [
        {
            'type': 'meeting',
            'icon': 'fa-users',
            'titre': 'Réunion des professeurs',
            'description': 'Réunion hebdomadaire avec l\'équipe pédagogique',
            'date': 'Lundi 15/01',
            'heure': '12h00-13h00'
        },
        {
            'type': 'event',
            'icon': 'fa-calendar-check',
            'titre': 'Conseil de classe',
            'description': 'Conseil de classe de la 6ème A',
            'date': 'Mardi 16/01',
            'heure': '16h00-17h00'
        },
        {
            'type': 'duty',
            'icon': 'fa-user-shield',
            'titre': 'Surveillance récréation',
            'description': 'Surveillance de la cour de récréation',
            'date': 'Mercredi 17/01',
            'heure': '10h00-10h15'
        }
    ]

    # Date de la semaine actuelle
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    semaine_actuelle = f"{start_of_week.strftime('%d/%m/%Y')} - {(start_of_week + timedelta(days=6)).strftime('%d/%m/%Y')}"

    return render_template('professeurs/emploi-du-temps.html',
                         horaires=horaires,
                         emploi_du_temps=emploi_du_temps,
                         activites=activites,
                         semaine_actuelle=semaine_actuelle)

# Routes pour les élèves
@app.route('/eleve/dashboard')
@login_required
def eleve_dashboard():
    if current_user.role != 'eleve':
        flash('Accès non autorisé')
        return redirect(url_for('login'))
    return render_template('eleves/dashboard.html')

@app.route('/eleve/resultats')
@login_required
def eleve_resultats():
    if current_user.role != 'eleve':
        flash('Accès non autorisé')
        return redirect(url_for('login'))
    return render_template('eleves/resultats.html')

@app.route('/eleve/emploi-du-temps')
@login_required
def eleve_emploi_du_temps():
    if current_user.role != 'eleve':
        flash('Accès non autorisé')
        return redirect(url_for('login'))
    return render_template('eleves/emploi_du_temps.html')

@app.route('/eleve/classement')
@login_required
def eleve_classement():
    if current_user.role != 'eleve':
        flash('Accès non autorisé')
        return redirect(url_for('login'))
    return render_template('eleves/classement.html')

@app.route('/eleve/messagerie')
@login_required
def eleve_messagerie():
    if current_user.role != 'eleve':
        flash('Accès non autorisé')
        return redirect(url_for('login'))
    return render_template('eleves/messagerie.html')

@app.route('/eleve/annonces')
@login_required
def eleve_annonces():
    if current_user.role != 'eleve':
        flash('Accès non autorisé')
        return redirect(url_for('login'))
    annonces = Annonce.query.order_by(Annonce.date_creation.desc()).all()
    return render_template('eleves/annonces.html', annonces=annonces)

@app.route('/eleve/annonces/<int:annonce_id>/commenter', methods=['POST'])
def ajouter_commentaire(annonce_id):
    if request.method == 'POST':
        contenu = request.form.get('contenu')
        eleve_id = request.form.get('eleve_id')  # À récupérer depuis la session
        
        if not contenu:
            return jsonify({'success': False, 'message': 'Le commentaire ne peut pas être vide'})
        
        try:
            nouveau_commentaire = Commentaire(
                contenu=contenu,
                date_creation=datetime.now(),
                eleve_id=eleve_id,
                annonce_id=annonce_id
            )
            db.session.add(nouveau_commentaire)
            db.session.commit()
            
            # Récupérer les informations de l'élève pour la réponse
            eleve = Eleve.query.get(eleve_id)
            
            return jsonify({
                'success': True,
                'commentaire': {
                    'contenu': contenu,
                    'date': datetime.now().strftime('%d/%m/%Y %H:%M'),
                    'auteur': f"{eleve.nom} {eleve.prenom}",
                    'avatar': eleve.avatar_url or 'https://via.placeholder.com/40'
                }
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Erreur lors de l\'ajout du commentaire'})

@app.route('/eleve/commentaires/<int:commentaire_id>', methods=['DELETE'])
def supprimer_commentaire(commentaire_id):
    commentaire = Commentaire.query.get_or_404(commentaire_id)
    eleve_id = request.form.get('eleve_id')  # À récupérer depuis la session
    
    # Vérifier si l'élève est l'auteur du commentaire
    if commentaire.eleve_id != eleve_id:
        return jsonify({'success': False, 'message': 'Vous n\'êtes pas autorisé à supprimer ce commentaire'})
    
    try:
        db.session.delete(commentaire)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Erreur lors de la suppression du commentaire'})

@app.route('/eleve/annonces/<int:annonce_id>/sauvegarder', methods=['POST'])
def sauvegarder_annonce(annonce_id):
    eleve_id = request.form.get('eleve_id')  # À récupérer depuis la session
    
    try:
        # Vérifier si l'annonce est déjà sauvegardée
        annonce = Annonce.query.get_or_404(annonce_id)
        if eleve_id in annonce.eleves_sauvegardee:
            # Retirer la sauvegarde
            annonce.eleves_sauvegardee.remove(eleve_id)
            action = 'retirée'
        else:
            # Ajouter la sauvegarde
            annonce.eleves_sauvegardee.append(eleve_id)
            action = 'sauvegardée'
        
        db.session.commit()
        return jsonify({'success': True, 'action': action})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Erreur lors de la sauvegarde de l\'annonce'})

@app.route('/eleve/annonces/<int:annonce_id>/inscrire', methods=['POST'])
def s_inscrire_evenement(annonce_id):
    eleve_id = request.form.get('eleve_id')  # À récupérer depuis la session
    
    try:
        annonce = Annonce.query.get_or_404(annonce_id)
        if not annonce.est_evenement:
            return jsonify({'success': False, 'message': 'Cette annonce n\'est pas un événement'})
        
        if eleve_id in annonce.eleves_inscrits:
            # Se désinscrire
            annonce.eleves_inscrits.remove(eleve_id)
            action = 'désinscrit'
        else:
            # S'inscrire
            annonce.eleves_inscrits.append(eleve_id)
            action = 'inscrit'
        
        db.session.commit()
        return jsonify({'success': True, 'action': action})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Erreur lors de l\'inscription à l\'événement'})

@app.route('/ecole/modifier-eleve', methods=['POST'])
@login_required
def modifierEleveEcole():
    print("Début de la fonction modifierEleveEcole")
    if current_user.role != 'admin':
        print("Accès non autorisé - Rôle:", current_user.role)
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))
    
    try:
        eleve_id = request.form.get('eleve_id')
        print(f"ID de l'élève à modifier: {eleve_id}")
        eleve = Eleve.query.get_or_404(eleve_id)
        print(f"Élève trouvé: {eleve.nom} {eleve.prenom}")
        
        # Récupérer l'école de l'administrateur
        ecole = Ecole.query.first()  # Pour l'instant, on prend la première école
        if not ecole:
            print("Aucune école trouvée")
            flash('Aucune école trouvée', 'error')
            return redirect(url_for('elevesAdmEcole'))
        
        # Vérifier que l'élève appartient à l'école
        if eleve.ecole_id != ecole.id:
            print(f"Accès non autorisé - École de l'élève: {eleve.ecole_id}, École: {ecole.id}")
            flash('Accès non autorisé', 'error')
            return redirect(url_for('elevesAdmEcole'))
        
        # Mettre à jour les informations de l'élève
        print("Données reçues du formulaire:")
        print(f"Nom: {request.form.get('nom')}")
        print(f"Prénom: {request.form.get('prenom')}")
        print(f"Date de naissance: {request.form.get('date_naissance')}")
        print(f"Classe ID: {request.form.get('classe_id')}")
        print(f"Parent nom: {request.form.get('parent_nom')}")
        print(f"Parent prénom: {request.form.get('parent_prenom')}")
        
        eleve.nom = request.form.get('nom')
        eleve.prenom = request.form.get('prenom')
        date_naissance = request.form.get('date_naissance')
        if date_naissance:
            eleve.date_naissance = datetime.strptime(date_naissance, '%Y-%m-%d').date()
        eleve.classe_id = request.form.get('classe_id')
        
        # Mettre à jour ou créer le parent
        parent_nom = request.form.get('parent_nom')
        parent_prenom = request.form.get('parent_prenom')
        parent_email = request.form.get('parent_email')
        parent_telephone = request.form.get('parent_telephone')
        
        if parent_nom and parent_prenom:
            if eleve.parent:
                print("Mise à jour du parent existant")
                # Mettre à jour le parent existant
                parent = eleve.parent
                parent.nom = parent_nom
                parent.prenom = parent_prenom
                parent.email = parent_email
                parent.telephone = parent_telephone
            else:
                print("Création d'un nouveau parent")
                # Créer un nouveau parent
                parent = Parent(
                    nom=parent_nom,
                    prenom=parent_prenom,
                    email=parent_email,
                    telephone=parent_telephone
                )
                db.session.add(parent)
                db.session.flush()  # Pour obtenir l'ID du parent
                eleve.parent_id = parent.id
        
        print("Tentative de commit des modifications")
        db.session.commit()
        print("Modifications enregistrées avec succès")
        flash('Les informations de l\'élève ont été mises à jour avec succès', 'success')
        
    except Exception as e:
        print(f"ERREUR lors de la modification: {str(e)}")
        print(f"Type d'erreur: {type(e)}")
        import traceback
        print(f"Traceback complet:\n{traceback.format_exc()}")
        db.session.rollback()
        flash(f'Une erreur est survenue lors de la modification : {str(e)}', 'error')
    
    return redirect(url_for('elevesAdmEcole'))

@app.route('/ecole/supprimer-eleve', methods=['POST'])
@login_required
def supprimerEleveEcole():
    print("Début de la fonction supprimerEleveEcole")
    if current_user.role != 'admin':
        print("Accès non autorisé - Rôle:", current_user.role)
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))
    
    try:
        eleve_id = request.form.get('eleve_id')
        print(f"ID de l'élève à supprimer: {eleve_id}")
        eleve = Eleve.query.get_or_404(eleve_id)
        print(f"Élève trouvé: {eleve.nom} {eleve.prenom}")
        
        # Récupérer l'école
        ecole = Ecole.query.first()
        if not ecole:
            print("Aucune école trouvée")
            flash('Aucune école trouvée', 'error')
            return redirect(url_for('elevesAdmEcole'))
        
        # Vérifier que l'élève appartient à l'école
        if eleve.ecole_id != ecole.id:
            print(f"Accès non autorisé - École de l'élève: {eleve.ecole_id}, École: {ecole.id}")
            flash('Accès non autorisé', 'error')
            return redirect(url_for('elevesAdmEcole'))
        
        # Supprimer l'élève
        print("Suppression de l'élève")
        db.session.delete(eleve)
        db.session.commit()
        print("Élève supprimé avec succès")
        flash('L\'élève a été supprimé avec succès', 'success')
        
    except Exception as e:
        print(f"ERREUR lors de la suppression: {str(e)}")
        print(f"Type d'erreur: {type(e)}")
        import traceback
        print(f"Traceback complet:\n{traceback.format_exc()}")
        db.session.rollback()
        flash(f'Une erreur est survenue lors de la suppression : {str(e)}', 'error')
    
    return redirect(url_for('elevesAdmEcole'))

# Route pour modifier un professeur
@app.route("/ecole/modifier-professeur", methods=['POST'])
@login_required
def modifierProfesseurEcole():
    if current_user.role != 'admin':
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))
    
    try:
        professeur_id = request.form.get('professeur_id')
        professeur = Professeur.query.get_or_404(professeur_id)
        
        # Mettre à jour les informations
        professeur.nom = request.form.get('nom')
        professeur.prenom = request.form.get('prenom')
        professeur.email = request.form.get('email')
        professeur.telephone = request.form.get('telephone')
        professeur.matieres = request.form.get('matieres')
        professeur.classes = request.form.get('classes')
        
        db.session.commit()
        flash('Professeur modifié avec succès', 'success')
        
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la modification du professeur: {str(e)}")
        flash('Erreur lors de la modification du professeur', 'error')
    
    return redirect(url_for('professeursEcole'))

# Route pour supprimer un professeur
@app.route("/ecole/supprimer-professeur", methods=['POST'])
@login_required
def supprimerProfesseurEcole():
    if current_user.role != 'admin':
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))
    
    try:
        professeur_id = request.form.get('professeur_id')
        professeur = Professeur.query.get_or_404(professeur_id)
        
        db.session.delete(professeur)
        db.session.commit()
        flash('Professeur supprimé avec succès', 'success')
        
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la suppression du professeur: {str(e)}")
        flash('Erreur lors de la suppression du professeur', 'error')
    
    return redirect(url_for('professeursEcole'))

# Route pour voir le profil d'un professeur
@app.route("/ecole/professeur/<int:professeur_id>")
@login_required
def professeurXEcole(professeur_id):
    if current_user.role != 'admin':
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))
    
    professeur = Professeur.query.get_or_404(professeur_id)
    return render_template('admEcole/professeurX.html', professeur=professeur)

@app.route("/ecole/classes")
@login_required
def classesEcole():
    if current_user.role != 'admin':
        flash('Accès non autorisé', 'error')
        return redirect(url_for('indexEcole'))
        
    # Récupérer l'école
    ecole = Ecole.query.first()
    if not ecole:
        flash('Aucune école trouvée', 'error')
        return redirect(url_for('indexEcole'))
    
    # Récupérer toutes les classes de l'école
    classes = Classe.query.filter_by(ecole_id=ecole.id).all()
    
    # Calculer le nombre d'élèves par classe
    for classe in classes:
        classe.nombre_eleves = Eleve.query.filter_by(classe_id=classe.id).count()
    
    return render_template("admEcole/classes.html", classes=classes)

@app.route("/ecole/classes/<int:classe_id>/details")
@login_required
def classeDetails(classe_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Accès non autorisé'}), 403
    
    # Récupérer la classe
    classe = Classe.query.get_or_404(classe_id)
    
    # Récupérer les élèves de la classe
    eleves = Eleve.query.filter_by(classe_id=classe.id).all()
    eleves_data = [{
        'id': eleve.id,
        'nom': eleve.nom,
        'prenom': eleve.prenom,
        'date_naissance': eleve.date_naissance.strftime('%d/%m/%Y') if eleve.date_naissance else ''
    } for eleve in eleves]
    
    # Récupérer les professeurs de la classe via la table Cours
    professeurs = Professeur.query.join(Cours).filter(Cours.classe_id == classe.id).all()
    professeurs_data = [{
        'id': prof.id,
        'nom': prof.nom,
        'prenom': prof.prenom,
        'matiere': prof.specialite  # Utiliser specialite au lieu de matiere
    } for prof in professeurs]
    
    return jsonify({
        'id': classe.id,
        'nom': classe.nom,
        'niveau': classe.niveau,
        'eleves': eleves_data,
        'professeurs': professeurs_data
    })

@app.route("/ecole/classes/ajouter", methods=['POST'])
@login_required
def ajouterClasseEcole():
    if current_user.role != 'admin':
        flash('Accès non autorisé', 'error')
        return redirect(url_for('indexEcole'))
    
    try:
        # Récupérer les données du formulaire
        nom = request.form.get('nom')
        niveau = request.form.get('niveau')
        capacite = request.form.get('capacite')
        annee_scolaire = request.form.get('annee_scolaire')
        
        # Récupérer l'école
        ecole = Ecole.query.first()
        if not ecole:
            flash('Aucune école trouvée', 'error')
            return redirect(url_for('classesEcole'))
        
        # Créer la nouvelle classe
        nouvelle_classe = Classe(
            nom=nom,
            niveau=niveau,
            capacite=capacite,
            annee_scolaire=annee_scolaire,
            ecole_id=ecole.id
        )
        
        db.session.add(nouvelle_classe)
        db.session.commit()
        flash('Classe ajoutée avec succès', 'success')
        
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de l'ajout de la classe: {str(e)}")
        flash('Erreur lors de l\'ajout de la classe', 'error')
    
    return redirect(url_for('classesEcole'))

@app.route("/ecole/classes/supprimer", methods=['POST'])
@login_required
def supprimerClasseEcole():
    if current_user.role != 'admin':
        flash('Accès non autorisé', 'error')
        return redirect(url_for('indexEcole'))
    
    try:
        classe_id = request.form.get('classe_id')
        classe = Classe.query.get_or_404(classe_id)
        
        # Vérifier qu'il n'y a pas d'élèves dans la classe
        if Eleve.query.filter_by(classe_id=classe_id).count() > 0:
            flash('Impossible de supprimer une classe contenant des élèves', 'error')
            return redirect(url_for('classesEcole'))
        
        db.session.delete(classe)
        db.session.commit()
        flash('Classe supprimée avec succès', 'success')
        
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la suppression de la classe: {str(e)}")
        flash('Erreur lors de la suppression de la classe', 'error')
    
    return redirect(url_for('classesEcole'))

@app.route('/ecole/annonces', methods=['GET'])
@login_required
def getAnnonces():
    if current_user.role != 'admin':
        return jsonify({'error': 'Non autorisé'}), 403
    
    # Récupérer l'école
    ecole = Ecole.query.first()
    if not ecole:
        return jsonify({'error': 'Aucune école trouvée'}), 404
    
    # Récupérer les annonces de l'école
    annonces = Annonce.query.filter_by(ecole_id=ecole.id).order_by(Annonce.date_creation.desc()).all()
    
    return jsonify([{
        'id': annonce.id,
        'titre': annonce.titre,
        'contenu': annonce.contenu,
        'date_creation': annonce.date_creation.isoformat(),
        'date_publication': annonce.date_publication.isoformat() if annonce.date_publication else None,
        'type_destinataire': annonce.type_destinataire,
        'priorite': annonce.priorite,
        'auteur_id': annonce.auteur_id
    } for annonce in annonces])

@app.route('/ecole/annonces', methods=['POST'])
@login_required
def createAnnonce():
    if current_user.role != 'admin':
        return jsonify({'error': 'Non autorisé'}), 403
    
    try:
        data = request.get_json()
        
        # Récupérer l'école
        ecole = Ecole.query.first()
        if not ecole:
            return jsonify({'error': 'Aucune école trouvée'}), 404
        
        # Créer la nouvelle annonce
        nouvelle_annonce = Annonce(
            ecole_id=ecole.id,
            titre=data['titre'],
            contenu=data['contenu'],
            date_creation=datetime.now(),
            date_publication=datetime.fromisoformat(data['date_publication']),
            type_destinataire=data['destinataires'],
            priorite=data['importance'],
            auteur_id=current_user.id
        )
        
        db.session.add(nouvelle_annonce)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Annonce créée avec succès',
            'annonce': {
                'id': nouvelle_annonce.id,
                'titre': nouvelle_annonce.titre,
                'contenu': nouvelle_annonce.contenu,
                'date_creation': nouvelle_annonce.date_creation.isoformat(),
                'date_publication': nouvelle_annonce.date_publication.isoformat(),
                'type_destinataire': nouvelle_annonce.type_destinataire,
                'priorite': nouvelle_annonce.priorite
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/ecole/annonces/<int:annonce_id>', methods=['PUT'])
@login_required
def updateAnnonce(annonce_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Non autorisé'}), 403
    
    try:
        # Récupérer l'école
        ecole = Ecole.query.first()
        if not ecole:
            return jsonify({'error': 'Aucune école trouvée'}), 404
            
        annonce = Annonce.query.get_or_404(annonce_id)
        if annonce.ecole_id != ecole.id:
            return jsonify({'error': 'Non autorisé'}), 403
        
        data = request.get_json()
        print(f"Données reçues pour la modification: {data}")
        
        # Mettre à jour l'annonce
        annonce.titre = data['titre']
        annonce.contenu = data['contenu']
        annonce.date_publication = datetime.fromisoformat(data['date_publication'])
        annonce.type_destinataire = data['destinataires']
        annonce.priorite = data['importance']
        
        # Si l'annonce est destinée à des classes spécifiques
        if data['destinataires'] == 'classes' and 'classes' in data:
            annonce.classes = []
            for classe_id in data['classes']:
                classe = Classe.query.get(classe_id)
                if classe:
                    annonce.classes.append(classe)
        
        db.session.commit()
        print("Annonce mise à jour avec succès")
        
        return jsonify({
            'success': True,
            'message': 'Annonce mise à jour avec succès',
            'annonce': {
                'id': annonce.id,
                'titre': annonce.titre,
                'contenu': annonce.contenu,
                'date_creation': annonce.date_creation.isoformat(),
                'date_publication': annonce.date_publication.isoformat(),
                'type_destinataire': annonce.type_destinataire,
                'priorite': annonce.priorite
            }
        })
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la mise à jour de l'annonce: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/ecole/annonces/<int:annonce_id>', methods=['DELETE'])
@login_required
def deleteAnnonce(annonce_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Non autorisé'}), 403
    
    try:
        # Récupérer l'école
        ecole = Ecole.query.first()
        if not ecole:
            return jsonify({'error': 'Aucune école trouvée'}), 404
            
        annonce = Annonce.query.get_or_404(annonce_id)
        if annonce.ecole_id != ecole.id:
            return jsonify({'error': 'Non autorisé'}), 403
        
        db.session.delete(annonce)
        db.session.commit()
        print(f"Annonce {annonce_id} supprimée avec succès")
        
        return jsonify({
            'success': True,
            'message': 'Annonce supprimée avec succès'
        })
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la suppression de l'annonce: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/ecole/annonces/<int:annonce_id>', methods=['GET'])
@login_required
def getAnnonce(annonce_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Non autorisé'}), 403
    
    try:
        # Récupérer l'école
        ecole = Ecole.query.first()
        if not ecole:
            return jsonify({'error': 'Aucune école trouvée'}), 404
            
        annonce = Annonce.query.get_or_404(annonce_id)
        if annonce.ecole_id != ecole.id:
            return jsonify({'error': 'Non autorisé'}), 403
        
        return jsonify({
            'id': annonce.id,
            'titre': annonce.titre,
            'contenu': annonce.contenu,
            'date_creation': annonce.date_creation.isoformat(),
            'date_publication': annonce.date_publication.isoformat() if annonce.date_publication else None,
            'type_destinataire': annonce.type_destinataire,
            'priorite': annonce.priorite,
            'auteur_id': annonce.auteur_id,
            'classes': [classe.id for classe in annonce.classes] if annonce.type_destinataire == 'classes' else []
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Routes pour la messagerie
@app.route('/api/messages', methods=['GET'])
@login_required
def get_messages():
    try:
        print(f"Récupération des messages pour l'utilisateur {current_user.id}")
        
        # Récupérer tous les messages où l'utilisateur est soit l'expediteur soit le destinataire
        messages = Message.query.filter(
            (Message.destinataire_id == current_user.id) | 
            (Message.expediteur_id == current_user.id)
        ).order_by(Message.date_envoi.desc()).all()
        
        print(f"Nombre de messages trouvés : {len(messages)}")
        
        # Convertir les messages en format JSON
        messages_list = []
        for msg in messages:
            message_data = {
                'id': msg.id,
                'sujet': msg.sujet,
                'contenu': msg.contenu,
                'date_envoi': msg.date_envoi.strftime('%Y-%m-%d %H:%M:%S'),
                'lu': msg.lu,
                'expediteur': {
                    'id': msg.expediteur.id,
                    'username': msg.expediteur.username
                },
                'destinataire': {
                    'id': msg.destinataire.id,
                    'username': msg.destinataire.username
                }
            }
            messages_list.append(message_data)
            print(f"Message ajouté : {message_data}")
        
        return jsonify(messages_list)
    except Exception as e:
        print(f"Erreur lors de la récupération des messages: {str(e)}")
        return jsonify([]), 200

@app.route('/api/messages/<int:message_id>', methods=['GET'])
@login_required
def get_message(message_id):
    try:
        print(f"Récupération du message {message_id} pour l'utilisateur {current_user.id}")
        
        message = Message.query.get_or_404(message_id)
        
        # Vérifier que l'utilisateur a le droit de voir ce message
        if message.destinataire_id != current_user.id and message.expediteur_id != current_user.id:
            print(f"Accès non autorisé au message {message_id}")
            return jsonify({'error': 'Accès non autorisé'}), 403
            
        # Marquer le message comme lu si l'utilisateur est le destinataire
        if message.destinataire_id == current_user.id and not message.lu:
            message.lu = True
            db.session.commit()
            print(f"Message {message_id} marqué comme lu")
        
        message_data = {
            'id': message.id,
            'sujet': message.sujet,
            'contenu': message.contenu,
            'date_envoi': message.date_envoi.strftime('%Y-%m-%d %H:%M:%S'),
            'lu': message.lu,
            'expediteur': {
                'id': message.expediteur.id,
                'username': message.expediteur.username
            },
            'destinataire': {
                'id': message.destinataire.id,
                'username': message.destinataire.username
            }
        }
        print(f"Message récupéré : {message_data}")
        
        return jsonify(message_data)
    except Exception as e:
        print(f"Erreur lors de la récupération du message: {str(e)}")
        return jsonify({'error': 'Message non trouvé'}), 404

@app.route('/api/messages/<int:message_id>', methods=['PUT'])
@login_required
def update_message(message_id):
    message = Message.query.get_or_404(message_id)
    
    # Vérifier que l'utilisateur est soit l'expéditeur soit le destinataire
    if message.expediteur_id != current_user.id and message.destinataire_id != current_user.id:
        return jsonify({'error': 'Accès non autorisé'}), 403
    
    data = request.get_json()
    
    # Mettre à jour les champs autorisés
    if 'statut' in data:
        message.statut = data['statut']
    
    db.session.commit()
    
    return jsonify({
        'id': message.id,
        'statut': message.statut
    })

@app.route('/api/messages/<int:message_id>', methods=['DELETE'])
@login_required
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    
    # Vérifier que l'utilisateur est soit l'expéditeur soit le destinataire
    if message.expediteur_id != current_user.id and message.destinataire_id != current_user.id:
        return jsonify({'error': 'Accès non autorisé'}), 403
    
    db.session.delete(message)
    db.session.commit()
    
    return '', 204

# Routes pour les groupes
@app.route('/api/groupes', methods=['GET'])
@login_required
def get_groupes():
    groupes = Groupe.query.filter_by(ecole_id=current_user.ecole_id).all()
    
    return jsonify([{
        'id': groupe.id,
        'nom': groupe.nom,
        'description': groupe.description,
        'date_creation': groupe.date_creation.strftime('%Y-%m-%d %H:%M:%S'),
        'membres': [{
            'id': membre.id,
            'username': membre.username
        } for membre in groupe.membres]
    } for groupe in groupes])

@app.route('/api/groupes', methods=['POST'])
@login_required
def create_groupe():
    data = request.get_json()
    
    groupe = Groupe(
        nom=data.get('nom'),
        description=data.get('description'),
        ecole_id=current_user.ecole_id
    )
    
    db.session.add(groupe)
    db.session.commit()
    
    # Ajouter l'utilisateur comme admin du groupe
    db.session.execute(
        groupes_membres.insert().values(
            groupe_id=groupe.id,
            user_id=current_user.id,
            role='admin'
        )
    )
    db.session.commit()
    
    return jsonify({
        'id': groupe.id,
        'nom': groupe.nom,
        'description': groupe.description,
        'date_creation': groupe.date_creation.strftime('%Y-%m-%d %H:%M:%S')
    }), 201

@app.route('/api/groupes/<int:groupe_id>/membres', methods=['POST'])
@login_required
def add_membre_groupe(groupe_id):
    groupe = Groupe.query.get_or_404(groupe_id)
    
    # Vérifier que l'utilisateur est admin du groupe
    membre = db.session.query(groupes_membres).filter_by(
        groupe_id=groupe_id,
        user_id=current_user.id,
        role='admin'
    ).first()
    
    if not membre:
        return jsonify({'error': 'Accès non autorisé'}), 403
    
    data = request.get_json()
    user_id = data.get('user_id')
    
    # Vérifier que l'utilisateur existe
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    # Ajouter l'utilisateur au groupe
    db.session.execute(
        groupes_membres.insert().values(
            groupe_id=groupe_id,
            user_id=user_id,
            role='membre'
        )
    )
    db.session.commit()
    
    return jsonify({
        'id': user.id,
        'username': user.username
    }), 201

# Ajout de la route pour enregistrer un nouveau message
@app.route('/ecole/messages/nouveau', methods=['POST'])
@login_required
def nouveauMessage():
    try:
        print("Réception d'une demande de nouveau message")
        data = request.get_json()
        print(f"Données reçues : {data}")
        
        # Vérifier que tous les champs requis sont présents
        if not all(k in data for k in ['destinataire_id', 'sujet', 'message']):
            print("Champs manquants dans la requête")
            return jsonify({'success': False, 'message': 'Tous les champs sont requis'}), 400
        
        # Créer le nouveau message
        nouveau_message = Message(
            expediteur_id=current_user.id,
            destinataire_id=data['destinataire_id'],
            sujet=data['sujet'],
            contenu=data['message'],
            date_envoi=datetime.utcnow(),
            lu=False
        )
        
        print(f"Création du message : {nouveau_message.__dict__}")
        
        # Sauvegarder dans la base de données
        db.session.add(nouveau_message)
        db.session.commit()
        
        print(f"Message créé avec succès, ID : {nouveau_message.id}")
        return jsonify({'success': True, 'message': 'Message envoyé avec succès'})
        
    except Exception as e:
        print(f"Erreur lors de la création du message : {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Erreur lors de l\'envoi du message'}), 500

@app.route('/api/conversations', methods=['GET'])
@login_required
def get_conversations():
    try:
        print(f"Récupération des conversations pour l'utilisateur {current_user.id}")
        
        # Récupérer tous les messages où l'utilisateur est soit l'expediteur soit le destinataire
        messages = Message.query.filter(
            (Message.destinataire_id == current_user.id) | 
            (Message.expediteur_id == current_user.id)
        ).order_by(Message.date_envoi.desc()).all()
        
        # Grouper les messages par conversation (même sujet)
        conversations = {}
        for msg in messages:
            if msg.sujet not in conversations:
                conversations[msg.sujet] = {
                    'id': msg.id,
                    'sujet': msg.sujet,
                    'date_envoi': msg.date_envoi,
                    'non_lu': msg.destinataire_id == current_user.id and not msg.lu,
                    'expediteur': {
                        'id': msg.expediteur.id,
                        'username': msg.expediteur.username
                    },
                    'contenu': msg.contenu
                }
        
        # Convertir le dictionnaire en liste et trier par date
        conversations_list = list(conversations.values())
        conversations_list.sort(key=lambda x: x['date_envoi'], reverse=True)
        
        print(f"Nombre de conversations trouvées : {len(conversations_list)}")
        return jsonify(conversations_list)
        
    except Exception as e:
        print(f"Erreur lors de la récupération des conversations: {str(e)}")
        return jsonify([]), 200

@app.route('/api/conversations/<int:conversation_id>', methods=['GET'])
@login_required
def get_conversation(conversation_id):
    try:
        print(f"Récupération de la conversation {conversation_id}")
        
        # Récupérer le message initial de la conversation
        initial_message = Message.query.get_or_404(conversation_id)
        
        # Vérifier que l'utilisateur a le droit de voir cette conversation
        if initial_message.destinataire_id != current_user.id and initial_message.expediteur_id != current_user.id:
            return jsonify({'error': 'Accès non autorisé'}), 403
        
        # Récupérer tous les messages liés à cette conversation (même sujet)
        messages = Message.query.filter_by(sujet=initial_message.sujet).order_by(Message.date_envoi.asc()).all()
        
        # Marquer les messages non lus comme lus
        for msg in messages:
            if msg.destinataire_id == current_user.id and not msg.lu:
                msg.lu = True
        db.session.commit()
        
        # Construire la réponse
        conversation_data = {
            'id': initial_message.id,
            'sujet': initial_message.sujet,
            'date_envoi': initial_message.date_envoi.strftime('%Y-%m-%d %H:%M:%S'),
            'expediteur': {
                'id': initial_message.expediteur.id,
                'username': initial_message.expediteur.username
            },
            'messages': [{
                'id': msg.id,
                'contenu': msg.contenu,
                'date_envoi': msg.date_envoi.strftime('%Y-%m-%d %H:%M:%S'),
                'expediteur_id': msg.expediteur_id,
                'destinataire_id': msg.destinataire_id
            } for msg in messages]
        }
        
        return jsonify(conversation_data)
        
    except Exception as e:
        print(f"Erreur lors de la récupération de la conversation: {str(e)}")
        return jsonify({'error': 'Conversation non trouvée'}), 404

# Routes pour les notes et bulletins
@app.route('/api/ecole/classes', methods=['GET'])
@login_required
def get_classes():
    try:
        # Récupérer l'école de l'utilisateur connecté
        ecole = Ecole.query.filter_by(directeur_id=current_user.id).first()
        if not ecole:
            return jsonify({'error': 'École non trouvée'}), 404
        
        # Récupérer toutes les classes de l'école
        classes = Classe.query.filter_by(ecole_id=ecole.id).all()
        
        # Formater les données pour la réponse
        classes_data = [{
            'id': classe.id,
            'nom': classe.nom,
            'niveau': classe.niveau,
            'annee_scolaire': classe.annee_scolaire,
            'professeur_principal': classe.professeur_principal.nom + ' ' + classe.professeur_principal.prenom if classe.professeur_principal else None,
            'capacite': classe.capacite
        } for classe in classes]
        
        return jsonify(classes_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ecole/matieres', methods=['GET'])
@login_required
def get_matieres():
    try:
        matieres = Matiere.query.filter_by(ecole_id=current_user.ecole_id).all()
        return jsonify([{
            'id': matiere.id,
            'nom': matiere.nom,
            'coefficient': matiere.coefficient
        } for matiere in matieres])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ecole/notes', methods=['GET'])
@login_required
def get_notes():
    try:
        classe_id = request.args.get('classe_id')
        matiere_id = request.args.get('matiere_id')
        trimestre = request.args.get('trimestre')

        query = Note.query.join(Eleve).filter(Eleve.ecole_id == current_user.ecole_id)
        
        if classe_id:
            query = query.filter(Eleve.classe_id == classe_id)
        if matiere_id:
            query = query.filter(Note.matiere_id == matiere_id)
        if trimestre:
            query = query.filter(Note.trimestre == trimestre)

        notes = query.all()
        
        return jsonify([{
            'id': note.id,
            'eleve_id': note.eleve_id,
            'eleve_nom': note.eleve.nom,
            'eleve_prenom': note.eleve.prenom,
            'matiere_id': note.matiere_id,
            'matiere_nom': note.matiere.nom,
            'valeur': note.valeur,
            'type_evaluation': note.type_evaluation,
            'trimestre': note.trimestre,
            'date_evaluation': note.date_evaluation.strftime('%Y-%m-%d'),
            'commentaire': note.commentaire
        } for note in notes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ecole/notes', methods=['POST'])
@login_required
def add_note():
    try:
        data = request.json
        nouvelle_note = Note(
            eleve_id=data['eleve_id'],
            matiere_id=data['matiere_id'],
            valeur=data['valeur'],
            type_evaluation=data['type_evaluation'],
            trimestre=data['trimestre'],
            date_evaluation=datetime.strptime(data['date_evaluation'], '%Y-%m-%d'),
            commentaire=data.get('commentaire', '')
        )
        db.session.add(nouvelle_note)
        db.session.commit()
        return jsonify({'message': 'Note ajoutée avec succès', 'id': nouvelle_note.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/ecole/notes/<int:note_id>', methods=['PUT'])
@login_required
def update_note(note_id):
    try:
        note = Note.query.get_or_404(note_id)
        data = request.json
        
        note.valeur = data.get('valeur', note.valeur)
        note.type_evaluation = data.get('type_evaluation', note.type_evaluation)
        note.trimestre = data.get('trimestre', note.trimestre)
        note.date_evaluation = datetime.strptime(data['date_evaluation'], '%Y-%m-%d') if 'date_evaluation' in data else note.date_evaluation
        note.commentaire = data.get('commentaire', note.commentaire)
        
        db.session.commit()
        return jsonify({'message': 'Note mise à jour avec succès'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/ecole/notes/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
    try:
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
        return jsonify({'message': 'Note supprimée avec succès'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/ecole/parametres-notes', methods=['GET'])
@login_required
def get_parametres_notes():
    # Récupérer l'école de l'utilisateur connecté
    ecole = Ecole.query.filter_by(directeur_id=current_user.id).first()
    if not ecole:
        return jsonify({'error': 'École non trouvée'}), 404
    
    return jsonify({
        'coefficients': ecole.coefficients_notes,
        'seuils_appreciation': ecole.seuils_appreciation
    })

@app.route('/api/ecole/parametres-notes', methods=['PUT'])
@login_required
def update_parametres_notes():
    # Récupérer l'école de l'utilisateur connecté
    ecole = Ecole.query.filter_by(directeur_id=current_user.id).first()
    if not ecole:
        return jsonify({'error': 'École non trouvée'}), 404
    
    data = request.get_json()
    
    # Mettre à jour les paramètres
    if 'coefficients' in data:
        ecole.coefficients_notes = data['coefficients']
    if 'seuils_appreciation' in data:
        ecole.seuils_appreciation = data['seuils_appreciation']
    
    try:
        db.session.commit()
        return jsonify({'message': 'Paramètres mis à jour avec succès'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)