from app import app, db, User

def create_admin():
    with app.app_context():
        # Vérifier si l'admin existe déjà
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # Créer l'admin
            admin = User(
                username='admin',
                email='admin@ecole.com',
                role='superadmin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Administrateur créé avec succès!")
        else:
            print("L'administrateur existe déjà!")

if __name__ == '__main__':
    create_admin() 