import jwt
import os
from models.clients import Client, Contract, Event, Company
from models.collaboration import Collaborator, Department
from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker
from DAO.company_dao import CompanyDAO

session = create_db_connection()

secret_key = os.environ.get('SECRET_KEY')
company_dao = CompanyDAO(session)


def get_id_by_token(token):
    decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
    collaborator_id = decoded_token['collaborator_id']
    return collaborator_id


def search_corresponding_client(client_name):
    #utiliser LA DAO
    clients_names_min = session.query(Client).filter(Client.full_name.ilike(f"%{client_name}%")).all()
    return clients_names_min

def search_corresponding_company(company_name):
    companys_names_min = session.query(Company).filter(Company.name.ilike(f"%{company_name}%")).all()
    return companys_names_min