import jwt
import os
from connect_database import create_db_connection

session = create_db_connection()

secret_key = os.environ.get('SECRET_KEY')


def get_id_by_token(token):
    """
    Retourne l'identifiant du collaborateur extrait du token JWT.
    """
    decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
    collaborator_id = decoded_token['collaborator_id']
    return collaborator_id
