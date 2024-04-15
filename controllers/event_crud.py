
from connect_database import create_db_connection
from utils.decorators import department_permission_required
from utils.get_object import get_id_by_token
from views.view_client import view_create_client, wich_customer, view_update_client
from DAO.client_dao import ClientDAO
from DAO.contract_dao import ContractDAO
from views.view_contract import view_create_contract, wich_contract, view_update_contract
from views.view_client import wich_customer
from views.login import login
from DAO.collaborator_dao import CollaboratorDAO
from DAO.client_dao import ClientDAO
from DAO.contract_dao import ContractDAO
from DAO.event_dao import EventDAO
from connect_database import create_db_connection
from tabulate import tabulate
from views.view_event import view_events, view_create_event, view_update_event, wich_event, view_delete_event, view_no_event_with_contract_unsigned

session = create_db_connection()
client_dao = ClientDAO(session)
collaborator_dao = CollaboratorDAO(session)
contract_dao = ContractDAO(session)
event_dao = EventDAO(session)


def display_all_events():
    events = event_dao.get_all_events()
    view_events(events)

def display_event_without_support(token):
    events = event_dao.get_events_without_support()
    view_events(events)

def display_my_events(token):
    collaborator_id = get_id_by_token(token)
    events = event_dao.get_events_by_collaborator_id(collaborator_id)
    view_events(events)


def create_event(token):
    created = False
    contract = wich_contract()
    if contract:
        if contract.status:
            client_id = contract.client_id
            client = client_dao.get_client(client_id)
            if client:
                event_data = view_create_event(client, contract, created)
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
                    created = True
                    view_create_event(client, contract, created)
            else:
                view_no_event_with_contract_unsigned(client, contract)



def update_event(token):
    client = wich_customer()
    contracts = contract_dao.get_contracts_by_client_id(client.id)
    events = []
    if contracts:
        for contract in contracts:
            event = event_dao.get_event_by_contract_id(contract.id).all()
            events.extend(event)
    event = wich_event(events, client.full_name)
    print("yup", event)

    if event:
        modified = False
        new_data = view_update_event(event, client.full_name, modified)
        if new_data:
            print(new_data)
            modification = event_dao.update_event(event.id, new_data)

            if modification:
                modified = True
                view_update_event(event, client.full_name, modified)


def delete_event(token):
    client = wich_customer()
    contracts = contract_dao.get_contracts_by_client_id(client.id)
    events = []
    if contracts:
        for contract in contracts:
            event = event_dao.get_event_by_contract_id(contract.id).all()
            events.extend(event)
    event = wich_event(events, client.full_name)

    if event:
        deleted = False
        response = view_delete_event(event, client, deleted)
        if response:
            remove = event_dao.delete_event(event.id)
            if remove:
                deleted = True
                view_delete_event(event, client, deleted)