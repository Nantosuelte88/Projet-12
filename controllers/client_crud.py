
from connect_database import create_db_connection
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from models.collaboration import Collaborator, Department
from models.clients import Client, Contract, Event
from datetime import datetime, timedelta, timezone
from utils.decorators import permission_for_commercial_department
from views.view_client import view_clients, view_create_client, view_wich_client, view_update_client, view_delete_client
from views.view_collaborator import view_not_authorized
from utils.get_object import get_id_by_token
from DAO.client_dao import ClientDAO
from DAO.company_dao import CompanyDAO
from DAO.contract_dao import ContractDAO
from DAO.event_dao import EventDAO
from DAO.collaborator_dao import CollaboratorDAO

session = create_db_connection()
client_dao = ClientDAO(session)
company_dao = CompanyDAO(session)
contract_dao =ContractDAO(session)
event_dao = EventDAO(session)
collaborator_dao = CollaboratorDAO(session)


def display_all_clients(token):
    # Récupérer tous les clients de la base de données
    clients = client_dao.get_all_clients()
    if clients:
        collaborators = []
        for client in clients:
            if client.commercial_id:
                collaborator = collaborator_dao.get_collaborator(client.commercial_id)
            else:
                collaborator = "Pas de collaborateur associé"
            collaborators.append(collaborator)
    view_clients(clients, collaborators)


def display_my_clients(token):
    collaborators = []
    collaborator_id = get_id_by_token(token)

    clients = client_dao.get_clients_by_collaborator_id(collaborator_id)
    if clients:
        collaborators = []
        for client in clients:
            if client.commercial_id:
                collaborator = collaborator_dao.get_collaborator(client.commercial_id)
            else:
                collaborator = "Pas de collaborateur associé"
            collaborators.append(collaborator)
    view_clients(clients, collaborators)

@permission_for_commercial_department()
def delete_client(token):
    client = wich_client()
    if client:
        user_id = get_id_by_token(token)
        if client.commercial_id == user_id:
            deleted = False
            contracts_clients = contract_dao.get_contracts_by_client_id(client.id)
            choice = view_delete_client(client, deleted, contracts_clients)
            if choice:
                remove = client_dao.delete_client(client.id)
                if remove:
                    deleted = True
                    view_delete_client(client, deleted, contracts_clients)
        else:
            view_not_authorized(client)

def last_contact_client(client_id):
    last_contact = datetime.now(timezone.utc)
    client = client_dao.get_client(client_id)
    if client:
        new_data = {'last_contact_date': last_contact}
        client_dao.update_client(client.id, new_data)


@permission_for_commercial_department()
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

@permission_for_commercial_department()
def update_client(token):
    modified = False
    client = wich_client()
    if client:
        user_id = get_id_by_token(token)
        if client.commercial_id == user_id:
            client_id = client.id
            response = view_update_client(client, modified)
            if response:
                if response.get("company_id"):
                    company_id = {'company_id': response.get("company_id")}
                    company_name = {'company_name': response.get("company_name")}
                    modified_client = client_dao.update_client(client_id, company_name)
                    modified_client = client_dao.update_client(client_id, company_id)
                else:
                    modified_client = client_dao.update_client(client_id, response)
                if modified_client:
                    modified = True
                    last_contact_client(client_id)
                    view_update_client(client, modified)
        else:
            view_not_authorized(client)

def wich_client():
    found = False
    clients_corresponding = None
    client_name = view_wich_client(clients_corresponding, found)
    if client_name:
        clients_corresponding = client_dao.get_clients_by_name(client_name)
        if clients_corresponding:
            found = True
            client = view_wich_client(clients_corresponding, found)
            if client:
                return client