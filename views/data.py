from controllers.auth_permissions import authenticate, authorize
from views.login import login
from models.clients import Client, Contract, Event
from models.collaboration import Collaborator, Department
from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker
from tabulate import tabulate
from utils.get_object import get_client_by_id, get_collaborator_by_id, get_contract_by_id
from utils.decorators import department_permission_required

session = create_db_connection()

@department_permission_required(None) 
def view_all_clients(token):
    #authorized = authorize(token, None)
    #if authorized:
    #    print('Autorisation ok')
    #else:
    #    print('Autorisation pas ok')

    # Récupérer tous les clients de la base de données
    clients = session.query(Client).all()

    if clients:
        # Préparer les données pour le tableau
        table_data = []
        for client in clients:
            collaborator = get_collaborator_by_id(client.commercial_id)
            row = [
                client.id,
                client.full_name,
                client.email,
                client.phone_number,
                client.company,
                client.creation_date,
                client.last_contact_date,
                collaborator.full_name if collaborator else "Commercial inconnu"
            ]
            table_data.append(row)

        # Afficher le tableau
        headers = [" ", "Nom", "Email", "Téléphone", "Nom de l'entreprise",
                "Date de création", "Dernier contact", "Contact commercial chez Epic Event"]
        print(tabulate(table_data, headers, tablefmt="grid"))
    else:
        print("Aucun client à afficher")



@department_permission_required(None) 
def view_all_contracts(token):

    # Récupérer tous les contrats de la base de données
    contracts = session.query(Contract).all()

    if contracts:
        # Préparer les données pour le tableau
        table_data = []
        # Afficher les informations des contrats
        for contract in contracts:
            client = get_client_by_id(contract.client_id)
            row = [
                contract.id,
                client.full_name if client else "Client inconnu",
                contract.total_amount,
                contract.remaining_amount,
                contract.creation_date,
                contract.status
            ]
            table_data.append(row)

            headers = [" ", "Client", "Montant total",
                        "Montant restant à payer", "Date de création", "Contrat signé"]
            print(tabulate(table_data, headers, tablefmt="grid"))
    else:
        print("Aucun contrat à afficher")


@department_permission_required(None) 
def view_all_events(token):
    events = session.query(Event).all()

    if events:
        table_data = []

        for event in events:
            contract = get_contract_by_id(event.contract_id)
            if contract:
                client = get_client_by_id(contract.client_id)

            support = get_collaborator_by_id(event.support_id)

            row = [
                event.id,
                event.name,
                event.contract_id,
                client.full_name if client else "Client inconnu",
                client.phone_number and client.email if client else "Client inconnu",
                event.date_start,
                event.date_end,
                support.full_name if support else "Support inconnu",
                event.location,
                event.attendees,
                event.notes
            ]
            table_data.append(row)

            headers = [" ", "Nom", "Contrat id", "Nom du client", "Contact du client", "Date de début",
                        "Date de fin", "Contact support chez Epic Event", "Lieu", "Nombres d'invités", "Commentaires"]
            print(tabulate(table_data, headers, tablefmt="grid"))
    else:
        print("Aucun événement à afficher")
