import os
import jwt
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, timezone
from connect_database import create_db_connection
from models.collaboration import Collaborator
import bcrypt

# Définir la session SQLAlchemy
engine = create_db_connection()
Session = sessionmaker(bind=engine)
session = Session()

secret_key = os.environ.get('SECRET_KEY')

def generate_token(collaborator_id, department_id):
    """
    Fonction pour générer le token JWT
    """
    # Définir les informations à inclure dans le token
    payload = {
        'collaborator_id': collaborator_id,
        'department_id': department_id,
        'exp': datetime.now(timezone.utc) + timedelta(hours=2)  # Définir une période d'expiration de 2 heures
    }
    
    # Générer le token en utilisant la clé secrète
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def authenticate(email, password):
    collaborator = session.query(Collaborator).filter_by(email=email).first()

    if collaborator:
        print('collab ok')
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
    
# Fonction pour l'autorisation
def authorize(token):
    try:
        # Vérifier la validité et l'intégrité du token
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        
        # Vérifier si le token a expiré
        if datetime.now(timezone.utc) > datetime.fromtimestamp(payload['exp']):
            return False

        # trouver comment acceder à l'id de department

        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    