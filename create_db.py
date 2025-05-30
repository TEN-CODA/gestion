import mysql.connector

# Connexion à MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="pmk007"
)

# Création du curseur
cursor = conn.cursor()

# Création de la base de données
cursor.execute("CREATE DATABASE IF NOT EXISTS gestion_ecole")

# Fermeture de la connexion
cursor.close()
conn.close()

print("Base de données créée avec succès!") 