from app import app, db
from models import User, Ecole, Eleve, Parent, Professeur, Classe, Matiere, Cours, Evaluation, Note
from datetime import datetime, date

def create_test_data():
    with app.app_context():
        # Créer une école
        ecole = Ecole(
            nom="École Test",
            adresse="123 Rue Test",
            telephone="0123456789",
            email="contact@ecole-test.com",
            date_creation=date.today()
        )
        db.session.add(ecole)
        db.session.commit()

        # Créer un professeur
        prof_user = User(
            username="prof1",
            email="prof1@ecole.com",
            role="professeur"
        )
        prof_user.set_password("prof123")
        db.session.add(prof_user)
        db.session.commit()

        professeur = Professeur(
            user_id=prof_user.id,
            ecole_id=ecole.id,
            nom="Dupont",
            prenom="Jean",
            specialite="Mathématiques",
            telephone="0123456789",
            email="prof1@ecole.com",
            date_embauche=date.today()
        )
        db.session.add(professeur)
        db.session.commit()

        # Créer une classe
        classe = Classe(
            ecole_id=ecole.id,
            nom="6ème A",
            niveau="6ème",
            annee_scolaire="2023-2024",
            professeur_principal_id=professeur.id,
            capacite=30
        )
        db.session.add(classe)
        db.session.commit()

        # Créer une matière
        matiere = Matiere(
            nom="Mathématiques",
            coefficient=4,
            description="Cours de mathématiques",
            ecole_id=ecole.id
        )
        db.session.add(matiere)
        db.session.commit()

        # Créer un cours
        cours = Cours(
            classe_id=classe.id,
            matiere_id=matiere.id,
            professeur_id=professeur.id,
            jour_semaine="Lundi",
            heure_debut=datetime.strptime("08:00", "%H:%M").time(),
            heure_fin=datetime.strptime("09:00", "%H:%M").time(),
            salle="Salle 101"
        )
        db.session.add(cours)
        db.session.commit()

        # Créer un parent
        parent_user = User(
            username="parent1",
            email="parent1@email.com",
            role="parent"
        )
        parent_user.set_password("parent123")
        db.session.add(parent_user)
        db.session.commit()

        parent = Parent(
            user_id=parent_user.id,
            nom="Martin",
            prenom="Sophie",
            telephone="0123456789",
            email="parent1@email.com",
            adresse="456 Rue Parent",
            profession="Ingénieur"
        )
        db.session.add(parent)
        db.session.commit()

        # Créer un élève
        eleve_user = User(
            username="eleve1",
            email="eleve1@ecole.com",
            role="eleve"
        )
        eleve_user.set_password("eleve123")
        db.session.add(eleve_user)
        db.session.commit()

        eleve = Eleve(
            user_id=eleve_user.id,
            ecole_id=ecole.id,
            nom="Martin",
            prenom="Lucas",
            date_naissance=date(2010, 1, 1),
            adresse="456 Rue Parent",
            telephone="0123456789",
            classe_id=classe.id,
            parent_id=parent.id
        )
        db.session.add(eleve)
        db.session.commit()

        print("Données de test créées avec succès!")

if __name__ == '__main__':
    create_test_data() 