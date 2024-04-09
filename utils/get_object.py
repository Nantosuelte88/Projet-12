import jwt
import os
from models.clients import Client, Contract, Event
from models.collaboration import Collaborator, Department
from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker


session = create_db_connection()

secret_key = os.environ.get('SECRET_KEY')


def get_id_by_token(token):
    decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
    collaborator_id = decoded_token['collaborator_id']
    return collaborator_id


def search_corresponding(client_name):
    clients_names_min = session.query(Client).filter(Client.full_name.ilike(client_name)).all()

    if clients_names_min:
        if len(clients_names_min) == 1:
            return True, clients_names_min[0]
        else:
            return True, clients_names_min
    else:
        return False, None