import logging
from sentry_sdk import capture_message
from connect_database import create_db_connection
import bcrypt
from DAO.collaborator_dao import CollaboratorDAO
from DAO.department_dao import DepartmentDAO

logger = logging.getLogger(__name__)

# Définissez la session SQLAlchemy
session = create_db_connection()

# Appelez les Dao de Departement et de Collaborateur
collaborator_dao = CollaboratorDAO(session)
department_dao = DepartmentDAO(session)


def create_departments():
    # Création des départements
    departments = ['support', 'gestion', 'commercial']

    for dept in departments:
        department_data = {
            'name': dept
        }
        response = department_dao.create_department(department_data)
        if response:
            print("Département créé avec succès !")
        else:
            print(f"Échec de création du département {dept}. Veuillez vérifier les données.")


def create_first_collaborator():
    # Définissez les informations pour créer le nouveau collaborateur
    full_name = "Nom prenom"
    email = "email@email.com"
    department_id = 2  # Attention de vérifier de bien mettre l'id du departement de gestion
    password = "motdepasse123"  # N'oubliez pas de modifier le mot de passe
    # Générez un sel (salt) aléatoire pour le hachage bcrypt
    salt = bcrypt.gensalt()
    # Hachez le mot de passe en utilisant bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    first_collaborateur_data = {
        'full_name': full_name,
        'email': email,
        'password': hashed_password,
        'department_id': department_id
    }

    first_collaborator = collaborator_dao.create_collaborator(
        first_collaborateur_data)
    if first_collaborator:
        # Message pour Sentry
        message = f"First collaborator created: {first_collaborator.full_name}, {first_collaborator.email}"
        logger.info(message)
        capture_message(message)
        print("Collaborateur crée avec succès")
