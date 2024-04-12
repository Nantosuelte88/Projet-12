import jwt
import os
from models.clients import Client, Contract, Event, Company
from models.collaboration import Collaborator, Department
from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker
from DAO.company_dao import CompanyDAO

session = create_db_connection()

secret_key = os.environ.get('SECRET_KEY')

def get_id_by_token(token):
    decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
    collaborator_id = decoded_token['collaborator_id']
    return collaborator_id
