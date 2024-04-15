
from connect_database import create_db_connection
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from models.collaboration import Collaborator, Department
from models.clients import Client, Contract, Event
from datetime import datetime, timedelta, timezone
from utils.decorators import department_permission_required
from views.view_client import view_create_client, wich_customer, view_update_client
from utils.get_object import get_id_by_token
from DAO.client_dao import ClientDAO
from DAO.company_dao import CompanyDAO
from DAO.contract_dao import ContractDAO
from views.view_contract import view_create_contract, wich_contract, view_update_contract, view_contracts, view_delete_contract


session = create_db_connection()
client_dao = ClientDAO(session)
company_dao = CompanyDAO(session)
contract_dao = ContractDAO(session)

def display_all_contracts(token):
    # Récupérer tous les contrats de la base de données
    contracts = contract_dao.get_all_contracts()
    view_contracts(contracts)


def display_contracts_unpaid(token):
    contracts = contract_dao.get_unpaid()
    view_contracts(contracts)

def display_unsigned_contracts(token):
    contracts = contract_dao.get_contract_unsigned()
    view_contracts(contracts)


def create_contract(token):
    client = wich_customer()
    if client:
        info_contract = view_create_contract(client)
        print(info_contract)
        if info_contract:
            creation_date = datetime.now(timezone.utc)

            new_contract_data ={
                'client_id': client.id,
                'total_amount': info_contract[0],
                'remaining_amount': info_contract[1],
                'creation_date': creation_date,
                'status': info_contract[2]
            }

            new_contract = contract_dao.create_contract(new_contract_data)

            if new_contract:
                print("Nouveau contrat enregistré avec succès")
            else:
                print("Une erreur s'est produite")

def update_contract(token):
    contract = wich_contract()
    print(contract)
    modified = False
    client = client_dao.get_client(contract.client_id)
    new_data = view_update_contract(contract, client.full_name, modified)
    if new_data:
        print(new_data)
        modification = contract_dao.update_contract(contract.id, new_data)

        if modification:
            modified = True
            view_update_contract(contract, client, modified)

def delete_contract(token):
    contract = wich_contract()
    if contract:
        deleted = False
        client = client_dao.get_client(contract.client_id)
        response = view_delete_contract(contract, client, deleted)
        if response:
            remove =contract_dao.delete_contract(contract.id)
            if remove:
                deleted = True
                view_delete_contract(contract, client, deleted)
