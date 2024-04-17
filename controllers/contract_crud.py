
from connect_database import create_db_connection
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from models.collaboration import Collaborator, Department
from models.clients import Client, Contract, Event
from datetime import datetime, timedelta, timezone
from utils.decorators import department_permission_required
from views.view_client import view_create_client, view_update_client
from utils.get_object import get_id_by_token
from DAO.client_dao import ClientDAO
from DAO.contract_dao import ContractDAO
from DAO.event_dao import EventDAO
from views.view_contract import view_create_contract, view_wich_contract, view_update_contract, view_contracts, view_delete_contract
from controllers.client_crud import last_contact_client, wich_client

session = create_db_connection()
client_dao = ClientDAO(session)
contract_dao = ContractDAO(session)
event_dao = EventDAO(session)


def display_all_contracts(token):
    # Récupérer tous les contrats de la base de données
    contracts = contract_dao.get_all_contracts()
    clients = []
    if contracts:
        for contract in contracts:
            client = client_dao.get_client(contract.client_id)
            clients.append(client)

    view_contracts(contracts, clients)


def display_contracts_unpaid(token):
    contracts = contract_dao.get_unpaid()
    clients = []
    if contracts:
        for contract in contracts:
            client = client_dao.get_client(contract.client_id)
            clients.append(client)

    view_contracts(contracts, clients)


def display_unsigned_contracts(token):
    contracts = contract_dao.get_contract_unsigned()
    clients = []
    if contracts:
        for contract in contracts:
            client = client_dao.get_client(contract.client_id)
            clients.append(client)

    view_contracts(contracts, clients)


def create_contract(token):
    client = wich_client()
    created = False
    if client:
        info_contract = view_create_contract(client, created)
        if info_contract:
            creation_date = datetime.now(timezone.utc)

            new_contract_data = {
                'client_id': client.id,
                'total_amount': info_contract[0],
                'remaining_amount': info_contract[1],
                'creation_date': creation_date,
                'status': info_contract[2]
            }

            new_contract = contract_dao.create_contract(new_contract_data)

            if new_contract:
                created = True
                view_create_contract(client, created)
                last_contact_client(client.id)


def update_contract(token):
    contract = wich_contract()
    modified = False
    client = client_dao.get_client(contract.client_id)
    new_data = view_update_contract(contract, client.full_name, modified)
    if new_data:
        modification = contract_dao.update_contract(contract.id, new_data)
        if 'client_id' in new_data:
            client_id = new_data['client_id']
        else:
            client_id = client.id
        if modification:
            modified = True
            view_update_contract(contract, client, modified)
            last_contact_client(client_id)


def delete_contract(token):
    contract = wich_contract()
    if contract:
        deleted = False
        client = client_dao.get_client(contract.client_id)
        events_client = event_dao.get_event_by_contract_id(contract.id)
        response = view_delete_contract(
            contract, client, deleted, events_client)
        if response:
            remove = contract_dao.delete_contract(contract.id)
            if remove:
                deleted = True
                view_delete_contract(contract, client, deleted, events_client)
                last_contact_client(client.id)


def wich_contract():
    client = wich_client()
    if client:
        contracts_corresponding = contract_dao.get_contracts_by_client_id(
            client.id)
        contract = view_wich_contract(contracts_corresponding, client)
        if contract:
            return contract
