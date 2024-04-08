import re
import getpass
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, timezone
from connect_database import create_db_connection
from models.collaboration import Collaborator
from controllers.auth_permissions import authenticate, authorize


def is_valid_email(email):
    """
    Vérifie si l'email est valide en utilisant une expression régulière
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


def is_valid_password(password):
    """
    Vérifie si le mot de passe est valide
    """
    # Exemple de règles de validation du mot de passe
    if len(password) < 10:
        return False

    return True


def login():
    """
    Permet de tester l'email et le mot de passe, reçoit le token
    """
    while True:
        print('Veuillez entrer vos identifiatns :')
        while True:
            email = input('votre email:')
            if is_valid_email(email):
                print('Email valide')
                break
            else:
                print('Veuillez entrer un email valide')

        while True:
            password = getpass.getpass('Votre mot de passe:')
            if is_valid_password(password):
                print('mdp à verifier')
                break
            else:
                print('Veuillez un mot de passe valide')

        if is_valid_email(email) and is_valid_password(password):
            token = authenticate(email, password)

            if token:
                authorized = authorize(token)
                if authorized:
                    print("Accès autorisé")
                    return token
                else:
                    print("Accès non autorisé")
            else:
                print("Échec de l'authentification")
