
from connect_database import create_db_connection
from utils.decorators import department_permission_required
from views.view_client import view_create_client, wich_customer, view_update_client
from utils.get_object import get_id_by_token
from DAO.client_dao import ClientDAO
from DAO.company_dao import CompanyDAO
from DAO.contract_dao import ContractDAO
from views.view_contract import view_create_contract, wich_contract, view_update_contract
from views.view_client import wich_customer
from views.login import login
from DAO.collaborator_dao import CollaboratorDAO
from DAO.client_dao import ClientDAO
from DAO.contract_dao import ContractDAO
from DAO.event_dao import EventDAO
from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker
from tabulate import tabulate
from utils.decorators import department_permission_required
from views.view_event import view_create_event

session = create_db_connection()
client_dao = ClientDAO(session)
collaborator_dao = CollaboratorDAO(session)
contract_dao = ContractDAO(session)
event_dao = EventDAO(session)

def create_event(token):
    contract = wich_contract()
    if contract:
        client_id = contract.client_id
        client = client_dao.get_client(client_id)
        if client:
            event_data = view_create_event(client, contract)
            print(event_data)
            support = event_data[6]
            if support:
                support_id = support
            else:
                support_id = None


            new_event_data = {
                'name': event_data[0],
                'contract_id': contract.id,
                'date_start': event_data[1],
                'date_end': event_data[2],
                'support_id': support_id,
                'location': event_data[3],
                'attendees': event_data[4],
                'notes': event_data[5]
            }

            new_event = event_dao.create_event(new_event_data)
            if new_event:
                print('yep', new_event)

def update_event(token):
    pass