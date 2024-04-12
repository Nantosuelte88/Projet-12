import click
from controllers.auth_permissions import authenticate, authorize
from views.login import login
from DAO.collaborator_dao import CollaboratorDAO
from DAO.client_dao import ClientDAO
from DAO.contract_dao import ContractDAO
from DAO.event_dao import EventDAO
from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker
from tabulate import tabulate
from utils.decorators import department_permission_required
from views.view_client import wich_customer
from utils.input_validators import is_valid_money_format

session = create_db_connection()
client_dao = ClientDAO(session)
collaborator_dao = CollaboratorDAO(session)
contract_dao = ContractDAO(session)
event_dao = EventDAO(session)


@department_permission_required(None) 
def view_all_contracts(token):

    # Récupérer tous les contrats de la base de données
    contracts = contract_dao.get_all_contracts()

    if contracts:
        # Préparer les données pour le tableau
        table_data = []
        # Afficher les informations des contrats
        for contract in contracts:
            client = client_dao.get_client(contract.client_id)
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

def view_create_contract(client):
    """
    Création d'un nouveau contrat
    """

    click.echo(f"Création d\'un nouveau contrat pour le client {client.full_name}")

    new_contract = []

    total_amount = click.prompt('Montant total', type=str)
    while not is_valid_money_format(total_amount):
        click.echo('Veuillez entrer une somme valide')
        total_amount = click.prompt('Montant total', type=str)
    new_contract.append(total_amount)

    remaining_amount = click.prompt('Reste à payer', type=str)
    while not is_valid_money_format(remaining_amount):
        click.echo('Veuillez entrer un somme valide')
        remaining_amount = click.prompt( 'Reste à payer', type=str)
    new_contract.append(remaining_amount)    

    status = click.prompt('Le contrat est-il signé? (O/N)', type=str)
    while status.upper() != 'O' and status.upper() != 'N':
        click.echo('Veuillez répondre par "O" pour Oui et "N" pour Non')
        status = click.prompt('Le contrat est-il signé? (O/N)', type=str)
    if status.upper() == 'O':
        status = True
    elif status.upper() == 'N':
        status = False
    new_contract.append(status)

    return new_contract

def wich_contract():
    client = wich_customer()

    if client:
        contracts = contract_dao.get_contracts_by_client_id(client.id)
        
        if contracts:
            click.echo(f"Contrat.s trouvé.s pour le client {client.full_name}:")
            for idx, contract in enumerate(contracts, start=1):
                click.echo(f"{idx}. ID du contrat : {contract.id}")
                click.echo(f"  - Mon total du contrat : {contract.total_amount}")
                if contract.status is True:
                    click.echo(f"  - Contrat signé")
                else:
                    click.echo("  - Contrat non signé")

           
            selected_idx = click.prompt("Entrez le numéro du contrat à modifier ", type=int)
            
            if 1 <= selected_idx <= len(contracts):
                selected_contract = contracts[selected_idx - 1]
                # Appeler une fonction pour modifier le contrat sélectionné
                return selected_contract
            else:
                click.echo("Numéro de contrat invalide.")
        else:
            click.echo("Aucun contrat trouvé pour ce client.")
    else:
        click.echo("Aucun client correspondant.")

def view_update_contract(contract, client_name, modified):

    if modified:
        click.echo("Contrat modifié avec succès")

    else:
        click.echo(f"Que souhaitez-vous modifier dans le contrat de {client_name}")
        click.echo(f'1: Le montant total : {contract.total_amount}')
        click.echo(f'2: le reste à payer : {contract.remaining_amount}')
        if contract.status is True:
            click.echo(f"3: le status du contrat : Contrat signé")
        else:
            click.echo(f"3: le status du contrat : Contrat non signé")

        choice = click.prompt("Entrez le numéro correspondant à votre choix: ", type=int)

        if choice == 1:
            new_total_amount = click.prompt("Entrez le nouveau montant total", type=str)
            while not is_valid_money_format(new_total_amount):
                click.echo('Veuillez entrer une nouvelle somme valide')
                new_total_amount = click.prompt("Entrez le nouveau montant total", type=str)

            contract_data = {'total_amount': new_total_amount}

        elif choice == 2:
            new_remaining_amount = click.prompt("Entrez un nouveau reste à charge: ", type=str)
            while not is_valid_money_format(new_remaining_amount):
                click.echo('Veuillez entrer une nouvelle somme valide')
                new_remaining_amount = click.prompt("Entrez un nouveau reste à charge: ", type=str)
            
            contract_data = {'remaining_amount': new_remaining_amount}

        elif choice == 3:
            new_status = click.prompt('Le contrat est-il signé? (O/N)', type=str)
            while new_status.upper() != 'O' and new_status.upper() != 'N':
                click.echo('Veuillez répondre par "O" pour Oui et "N" pour Non')
                new_status = click.prompt('Le contrat est-il signé? (O/N)', type=str)
            if new_status.upper() == 'O':
                new_status = True
            elif new_status.upper() == 'N':
                new_status = False
            contract_data = {'status': new_status}
        
        else:
            click.echo("Choix invalide.")
            return False

        return contract_data
        