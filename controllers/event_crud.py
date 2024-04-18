
from connect_database import create_db_connection
from utils.get_object import get_id_by_token
from utils.decorators import permission_for_gestion_department, permission_for_support_department, permission_for_commercial_department
from DAO.client_dao import ClientDAO
from DAO.contract_dao import ContractDAO
from DAO.collaborator_dao import CollaboratorDAO
from DAO.client_dao import ClientDAO
from DAO.contract_dao import ContractDAO
from DAO.event_dao import EventDAO
from connect_database import create_db_connection
from views.view_event import view_events, view_create_event, view_update_event, view_search_event_by_name_or_client, view_delete_event, view_no_event_with_contract_unsigned, view_wich_event, view_update_support_in_event, view_contract_has_event, view_no_event_update_for_wrong_support
from views.view_collaborator import view_not_authorized
from controllers.client_crud import last_contact_client, wich_client
from controllers.contract_crud import wich_contract

session = create_db_connection()
client_dao = ClientDAO(session)
collaborator_dao = CollaboratorDAO(session)
contract_dao = ContractDAO(session)
event_dao = EventDAO(session)


def display_all_events(token):
    events = event_dao.get_all_events()
    clients = []
    supports = []
    if events:
        for event in events:
            contract = contract_dao.get_contract(event.contract_id)
            if contract:
                client = client_dao.get_client(contract.client_id)
                clients.append(client)

            if event.support_id:
                support_obj = collaborator_dao.get_collaborator(event.support_id)
                support = support_obj.full_name
            else:
                support = "Pas de collaborateur associé"
            supports.append(support)

    view_events(events, clients, supports)

@permission_for_gestion_department()
def display_event_without_support(token):
    events = event_dao.get_events_without_support()
    view_events(events)

@permission_for_support_department()
def display_my_events(token):
    collaborator_id = get_id_by_token(token)
    events = event_dao.get_events_by_collaborator_id(collaborator_id)
    view_events(events)

@permission_for_commercial_department()
def create_event(token):
    created = False
    contract = wich_contract()
    if contract:
        contract_event = event_dao.get_event_by_contract_id(contract.id)
        if contract_event:
            view_contract_has_event(contract, contract_event)
        else:
            client_id = contract.client_id
            client = client_dao.get_client(client_id)
            if client:
                if contract.status:
                    user_id = get_id_by_token(token)
                    if client.commercial_id == user_id:
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
                            last_contact_client(client_id)
                            view_create_event(client, contract, created)
                    else:
                        view_not_authorized(client)
                else:
                    view_no_event_with_contract_unsigned(client, contract)

@permission_for_support_department()
def update_event(token):
    event = wich_event()
    if event:
        user_id = get_id_by_token(token)
        if event.support_id == user_id:
            contract = contract_dao.get_contract(event.contract_id)
            if contract:
                client = client_dao.get_client(contract.client_id)
                if client:
                    modified = False
                    new_data = view_update_event(event, client.full_name, modified)
                    if new_data:
                        if 'client_id' in new_data:
                            client_id = new_data['client_id']
                            modification = contract_dao.update_contract(event.contract_id, new_data)
                        else:
                            modification = event_dao.update_event(event.id, new_data)
                            client_id = client.id

                        if modification:
                            modified = True
                            view_update_event(event, client.full_name, modified)
                            last_contact_client(client_id)
        else:
            view_no_event_update_for_wrong_support(event)

@permission_for_gestion_department()
def update_support_in_event(token):
    event = wich_event()
    modified = False
    if event:
        support = collaborator_dao.get_collaborator(event.support_id)
        new_data = view_update_support_in_event(event, support, modified)
        if new_data:
            modification = event_dao.update_event(event.id, new_data)
            if modification:
                modified = True
                view_update_event(event, support, modified)


def delete_event(token):
    event = wich_event()
    contract = contract_dao.get_contract(event.contract_id)
    if contract:
        client = client_dao.get_client(contract.client_id)
        if client:
            if event:
                deleted = False
                response = view_delete_event(event, client, deleted)
                if response:
                    remove = event_dao.delete_event(event.id)
                    if remove:
                        deleted = True
                        view_delete_event(event, client, deleted)
                        last_contact_client(client.id)


def get_events_by_client(client):
    if client:
        contracts = contract_dao.get_contracts_by_client_id(client.id)
        events = []
        if contracts:
            for contract in contracts:
                event = event_dao.get_event_by_contract_id(contract.id).all()
                events.extend(event)
        return events


def wich_event():
    response = view_search_event_by_name_or_client()
    if response:
        if 'client_name' in response:
            client = wich_client()
            if client:
                events = get_events_by_client(client)
        elif 'name' in response:
            event_name = response['name']
            if event_name:
                events = event_dao.get_events_by_name(event_name)
        
        event = view_wich_event(events)
        if event:
            return event
    
    else:
        return None