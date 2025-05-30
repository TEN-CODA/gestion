import mysql.connector

# Connexion à MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="pmk007"
)

cursor = conn.cursor()

# Suppression de la base si elle existe
cursor.execute("DROP DATABASE IF EXISTS gestion_ecole")
print("Base de données supprimée (si elle existait).")

# Création de la base
cursor.execute("CREATE DATABASE gestion_ecole")
print("Base de données créée.")

cursor.close()
conn.close() 