from app import app, db, User, Ecole, Professeur, Parent

def create_initial_users():
    with app.app_context():
        # 1. Créer le superadmin
        superadmin = User.query.filter_by(username='superadmin').first()
        if not superadmin:
            superadmin = User(
                username='superadmin',
                email='superadmin@ecole.com',
                role='superadmin'
            )
            superadmin.set_password('superadmin123')
            db.session.add(superadmin)
            db.session.commit()
            print("Superadmin créé avec succès!")

        # 2. Créer une école et son admin
        ecole = Ecole.query.filter_by(nom='École Exemple').first()
        if not ecole:
            ecole = Ecole(
                nom='École Exemple',
                adresse='123 Rue de l\'École',
                telephone='0123456789',
                email='contact@ecole-exemple.com'
            )
            db.session.add(ecole)
            db.session.flush()  # Pour obtenir l'ID de l'école

            # Créer l'admin de l'école
            admin_ecole = User(
                username='admin_ecole',
                email='admin@ecole-exemple.com',
                role='admin_ecole'
            )
            admin_ecole.set_password('admin123')
            db.session.add(admin_ecole)
            db.session.commit()
            print("École et son admin créés avec succès!")

        # 3. Créer un professeur
        prof = User.query.filter_by(username='professeur').first()
        if not prof:
            prof = User(
                username='professeur',
                email='prof@ecole-exemple.com',
                role='professeur'
            )
            prof.set_password('prof123')
            db.session.add(prof)
            db.session.flush()

            professeur = Professeur(
                user_id=prof.id,
                ecole_id=ecole.id,
                nom='Dupont',
                prenom='Jean',
                specialite='Mathématiques',
                telephone='0123456789',
                email='prof@ecole-exemple.com'
            )
            db.session.add(professeur)
            db.session.commit()
            print("Professeur créé avec succès!")

        # 4. Créer un parent
        parent_user = User.query.filter_by(username='parent').first()
        if not parent_user:
            parent_user = User(
                username='parent',
                email='parent@example.com',
                role='parent'
            )
            parent_user.set_password('parent123')
            db.session.add(parent_user)
            db.session.flush()

            parent = Parent(
                user_id=parent_user.id,
                nom='Martin',
                prenom='Sophie',
                telephone='0123456789',
                email='parent@example.com',
                adresse='456 Rue des Parents',
                profession='Ingénieur'
            )
            db.session.add(parent)
            db.session.commit()
            print("Parent créé avec succès!")

if __name__ == '__main__':
    create_initial_users() 