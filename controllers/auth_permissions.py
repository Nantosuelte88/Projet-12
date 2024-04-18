import os
import jwt
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, timezone
from connect_database import create_db_connection
from models.collaboration import Collaborator
import bcrypt

# Définir la session SQLAlchemy
session = create_db_connection()

secret_key = os.environ.get('SECRET_KEY')


def generate_token(collaborator_id, department_id):
    """
    Fonction pour générer le token JWT
    """
    # Définir les informations à inclure dans le token
    payload = {
        'collaborator_id': collaborator_id,
        'department_id': department_id,
        # Définir une période d'expiration de 2 heures
        'exp': datetime.now(timezone.utc) + timedelta(hours=2)
    }

    # Générer le token en utilisant la clé secrète
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


def authenticate(email, password):
    collaborator = session.query(Collaborator).filter_by(email=email).first()

    if collaborator:
        print('collaborateur trouvé :', collaborator.full_name)
        if bcrypt.checkpw(password.encode('utf-8'), collaborator.password.encode('utf-8')):
            # Le mot de passe est valide
            print('Authentification réussie')
            token = generate_token(collaborator.id, collaborator.department_id)
            return token
        else:
            # Le mot de passe est incorrect
            print('Mot de passe incorrect')
    else:
        # L'utilisateur n'existe pas
        print('Utilisateur inconnu')
        return None


def authorize(token):
    try:
        # Vérifier la validité et l'intégrité du token
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        # Convertir l'objet de date et d'heure en UTC
        exp_time = datetime.fromtimestamp(payload['exp'], tz=timezone.utc)

        # Vérifier si le token a expiré
        if datetime.now(timezone.utc) > exp_time:
            # Le token a expiré, rafraîchir le token
            new_token = refresh_token(token)

            if new_token is None:
                # Gérer l'erreur de rafraîchissement du token
                return False

            # Utiliser le nouveau token rafraîchi
            token = new_token
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        return True

    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

def verify_department(token, department_id):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        user_department_id = payload['department_id']

        if user_department_id == department_id:
            return True

        return False

    except jwt.InvalidTokenError:
        return False
    

def refresh_token(old_token):
    try:
        # Décoder l'ancien token pour récupérer l'ID du collaborateur et l'ID du département
        payload = jwt.decode(old_token, secret_key, algorithms=['HS256'])

        # Vérifier si le token a expiré
        if datetime.now(timezone.utc) > datetime.fromtimestamp(payload['exp'], tz=timezone.utc):
            # Le token a expiré, générer un nouveau token
            collaborator_id = payload['collaborator_id']
            department_id = payload['department_id']
            new_token = generate_token(collaborator_id, department_id)
            return new_token

        # Si le token n'a pas expiré, renvoyer l'ancien token
        return old_token

    except jwt.InvalidTokenError:
        return None
