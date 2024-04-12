import click
from connect_database import create_db_connection
from utils.decorators import department_permission_required
from views.view_client import view_create_client, wich_customer, view_update_client
from utils.input_validators import is_valid_date_format
from DAO.client_dao import ClientDAO
from DAO.company_dao import CompanyDAO
from DAO.contract_dao import ContractDAO
from views.view_contract import view_create_contract, wich_contract, view_update_contract
from views.view_collaborator import wich_collaborator

from views.login import login
from DAO.collaborator_dao import CollaboratorDAO
from DAO.client_dao import ClientDAO
from DAO.contract_dao import ContractDAO
from DAO.event_dao import EventDAO
from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker
from tabulate import tabulate
from utils.decorators import department_permission_required

COMMERCIAL = 3
GESTION = 2
SUPPORT = 1



session = create_db_connection()
client_dao = ClientDAO(session)
collaborator_dao = CollaboratorDAO(session)
contract_dao = ContractDAO(session)
event_dao = EventDAO(session)

@department_permission_required(None) 
def view_all_events(token):
    events = event_dao.get_all_events()

    if events:
        table_data = []

        for event in events:
            contract = contract_dao.get_contract(event.contract_id)
            if contract:
                client = client_dao.get_client(contract.client_id)

            support = collaborator_dao.get_collaborator(event.support_id)

            row = [
                event.id,
                event.name,
                event.contract_id,
                client.full_name if client else "Client inconnu",
                f"{client.phone_number}\n{client.email}" if client else "Client inconnu",
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


def view_create_event(client, contract):
    click.echo(f"Création d'un nouvel evenement pour le client {client.full_name} sous contrat n°{contract.id}")

    new_event = []

    name = click.prompt('Nom de l\'événement', type=str)
    while not all(c.isalnum() or c.isspace() for c in name):
        click.echo('Veuillez entrer un nom valide')
        name = click.prompt('Nom de l\'événement', type=str)
    new_event.append(name)

    date_start = click.prompt('Date de début (AAAA-MM-JJ)', type=str)
    while not is_valid_date_format(date_start):
        click.echo('Veuillez entrer une date valide au format AAAA-MM-JJ')
        date_start = click.prompt('Date de début (AAAA-MM-JJ)', type=str)
    new_event.append(date_start)

    date_end = click.prompt('Date de fin (AAAA-MM-JJ)', type=str)
    while not is_valid_date_format(date_end):
        click.echo('Veuillez entrer une date valide au format AAAA-MM-JJ')
        date_end = click.prompt('Date de fin (AAAA-MM-JJ)', type=str)
    new_event.append(date_end)

    location = click.prompt('Le lieu de l\'événement', type=str)
    while not all(c.isalnum() or c.isspace() for c in location):
        click.echo('Veuillez entrer une donnée valide')
        location = click.prompt('Le lieu de l\'événement', type=str)
    new_event.append(location)

    attendees = click.prompt('Nombre de convives attendues', type=int)
    new_event.append(attendees)

    notes = click.prompt('Commentaire ', type=str)
    while not all(c.isalnum() or c.isspace() for c in notes):
        click.echo('Veuillez entrer une donnée valide')
        notes = click.prompt('Commentaire ', type=str)
    new_event.append(notes)

    response = click.prompt('Voulez-vous ajouter un collaborateur du département support ? (O/N)', type=str)
    while response.upper() != 'O' and response.upper() != 'N':
        click.echo('Veuillez répondre par "O" pour Oui et "N" pour Non')
        response = click.prompt('Voulez-vous ajouter un collaborateur du département support ? (O/N)', type=str)
    if response.upper() == 'O':
        collaborator_id = wich_collaborator(SUPPORT)
        click.echo(f'collabo : {collaborator_id}')
        if collaborator_id:
            collaborator = collaborator_id
        else:
            collaborator = None
    else:
        collaborator = None

    new_event.append(collaborator)

    return new_event

def view_update_event():
    pass