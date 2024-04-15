
from connect_database import create_db_connection
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from models.collaboration import Collaborator, Department
from models.clients import Client, Contract, Event
from datetime import datetime, timedelta, timezone
from utils.decorators import department_permission_required
from views.view_client import view_clients, view_create_client, wich_customer, view_update_client, view_delete_client
from utils.get_object import get_id_by_token
from DAO.client_dao import ClientDAO
from DAO.company_dao import CompanyDAO

session = create_db_connection()
client_dao = ClientDAO(session)
company_dao = CompanyDAO(session)


def display_all_clients(token):
    # Récupérer tous les clients de la base de données
    clients = client_dao.get_all_clients()
    view_clients(clients)


def display_my_clients(token):
    collaborator_id = get_id_by_token(token)
    clients = client_dao.get_clients_by_collaborator_id(collaborator_id)
    view_clients(clients)


def delete_client(token):
    client = wich_customer()
    deleted = False
    choice = view_delete_client(client, deleted)
    if choice:
        remove = client_dao.delete_client(client.id)
        if remove:
            deleted = True
            view_delete_client(client, deleted)


@department_permission_required(3)
def create_new_client(token):
    created = False
    info_client = view_create_client(created)
    if info_client:
        creation_date = datetime.now(timezone.utc)
        last_contact_date = None
        commercial_id = get_id_by_token(token)
        company_name = info_client[3]
        company_id = None

        if company_name and info_client[4]:
            company_id = info_client[4]

        # Création d'une instance du client avec les valeurs spécifiées
        new_client_data = {
            'full_name': info_client[0],
            'email': info_client[1],
            'phone_number': info_client[2],
            'creation_date': creation_date,
            'last_contact_date': last_contact_date,
            'commercial_id': commercial_id,
            'company_name': company_name,
            'company_id': company_id
        }

        # Appel à la méthode create_client du DAO pour créer le client
        new_client = client_dao.create_client(new_client_data)

        if new_client:
            created = True
            view_create_client(created)


def update_client(token):
    modified = False
    client = wich_customer()
    client_id = client.id
    response = view_update_client(client, modified)
    print("1;", response)
    print(response.get("company_id"))
    if response:
        if response.get("company_id"):
            company_id = {'company_id': response.get("company_id")}
            company_name = {'company_name': response.get("company_name")}
            modified_client = client_dao.update_client(client_id, company_name)
            modified_client = client_dao.update_client(client_id, company_id)
        else:
            modified_client = client_dao.update_client(client_id, response)
        print("2;", modified_client.company, modified_client.company_id)
        if modified_client:
            modified = True
            view_update_client(client, modified)