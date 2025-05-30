from app import app, db
from models import User, Ecole, Eleve, Parent, Professeur, Classe, Matiere, Cours, Evaluation, Note

def init_db():
    with app.app_context():
        # Créer toutes les tables
        db.create_all()
        print("Tables créées avec succès!")

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
    init_db() 