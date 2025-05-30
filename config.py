import os
from datetime import timedelta

class Config:
    # Configuration de base
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'votre-clé-secrète-ici'
    
    # Configuration de la base de données
    SQLALCHEMY_DATABASE_URI = 'mysql://root:pmk007@127.0.0.1:3306/gestion_ecole'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuration de la session
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    
    # Configuration des uploads
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    
    # Configuration des emails
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') 