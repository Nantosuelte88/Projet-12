import logging
from sentry_sdk import capture_message
from connect_database import create_db_connection
from datetime import datetime, timezone
from DAO.client_dao import ClientDAO
from DAO.contract_dao import ContractDAO
from DAO.event_dao import EventDAO
from DAO.collaborator_dao import CollaboratorDAO
from views.view_contract import view_create_contract, view_wich_contract, view_update_contract, view_contracts, view_delete_contract
from views.view_collaborator import view_not_authorized
from controllers.client_crud import last_contact_client, wich_client
from utils.decorators import permission_commercial_or_gestion, permission_for_gestion_department, permission_for_commercial_department, COMMERCIAL
from utils.get_object import get_id_by_token


logger = logging.getLogger(__name__)


session = create_db_connection()
client_dao = ClientDAO(session)
contract_dao = ContractDAO(session)
event_dao = EventDAO(session)
collaborator_dao = CollaboratorDAO(session)


def display_all_contracts(token):
    """
    Affiche tous les contrats de la base de données avec leurs clients associés.
    """
    contracts = contract_dao.get_all_contracts()
    clients = []
    if contracts:
        for contract in contracts:
            client = client_dao.get_client(contract.client_id)
            clients.append(client)

    view_contracts(contracts, clients)


@permission_for_commercial_department()
def display_contracts_unpaid(token):
    """
    Affiche tous les contrats impayés de la base de données avec leurs clients associés.
    """
    contracts = contract_dao.get_unpaid()
    clients = []
    if contracts:
        for contract in contracts:
            client = client_dao.get_client(contract.client_id)
            clients.append(client)

    view_contracts(contracts, clients)


@permission_for_commercial_department()
def display_unsigned_contracts(token):
    """
    Affiche tous les contrats non signés de la base de données avec leurs clients associés.
    """
    contracts = contract_dao.get_contract_unsigned()
    clients = []
    if contracts:
        for contract in contracts:
            client = client_dao.get_client(contract.client_id)
            clients.append(client)

    view_contracts(contracts, clients)


@permission_for_gestion_department()
def create_contract(token):
    """
    Crée un nouveau contrat en utilisant la date actuelle comme date de création.
    """
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

                # Si le contrat est signé -> message dans Sentry
                if info_contract[2]:
                    message = f"A new contract for {client.full_name} has been created and signed"
                    logger.info(message)
                    capture_message(message)


@permission_commercial_or_gestion()
def update_contract(token):
    """
    Modifie un contrat, en vérifiant l'autorisation appropriée pour le faire.
    Si l'utilisateur est un commercial, on vérifie qu'il est affilié au client concerné.
    """
    contract = wich_contract()
    if contract:
        modified = False
        collaborator_checked = False
        client = client_dao.get_client(contract.client_id)
        if client:

            # Si le collaborateur est un commercial -> on verifie que c'est celui affilié au client
            collaborator_id = get_id_by_token(token)
            collaborator = collaborator_dao.get_collaborator(collaborator_id)
            if collaborator:
                if collaborator.department_id == COMMERCIAL:
                    if collaborator.id == client.commercial_id:
                        collaborator_checked = True
                    else:
                        view_not_authorized(client)
                else:
                    collaborator_checked = True

            if collaborator_checked:
                new_data = view_update_contract(
                    contract, client.full_name, modified)
                if new_data:
                    modification = contract_dao.update_contract(
                        contract.id, new_data)
                    if 'client_id' in new_data:
                        client_id = new_data['client_id']
                    else:
                        client_id = client.id
                    if modification:
                        modified = True
                        view_update_contract(contract, client, modified)
                        last_contact_client(client_id)

                        # Si le contrat est signé -> message dans Sentry
                        if 'status' in new_data:
                            if new_data['status']:
                                message = f"Contract n°{contract.id} has been signed"
                                logger.info(message)
                                capture_message(message)

@permission_for_gestion_department()
def delete_contract(token):
    """ 
    Supprime un contrat de la base de données.
    """
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
    """
    Renvoie une liste de contrats correspondant au client sélectionné.
    """
    client = wich_client()
    if client:
        contracts_corresponding = contract_dao.get_contracts_by_client_id(
            client.id)
        contract = view_wich_contract(contracts_corresponding, client)
        if contract:
            return contract
