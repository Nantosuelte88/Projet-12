import click
from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker
from tabulate import tabulate
from utils.get_object import search_corresponding_client, search_corresponding_company
from utils.input_validators import is_valid_phone_number
from DAO.client_dao import ClientDAO
from DAO.collaborator_dao import CollaboratorDAO
from DAO.company_dao import CompanyDAO
from tabulate import tabulate

session = create_db_connection()
collaborator_dao = CollaboratorDAO(session)
client_dao = ClientDAO(session)
company_dao = CompanyDAO(session)

def wich_company(company_name):
    matching_companies = search_corresponding_company(company_name)
    if matching_companies:
        click.echo('Entreprises correspondante.s trouvée.s :')
        if len(matching_companies) == 1:
            click.echo("Une entreprise trouvée ")
            click.echo(f"{matching_companies[0].name}")

            response = click.prompt('Voulez-vous sélectionner cette entreprise ? (O/N)', type=str)
            if response.upper() == 'O':
                company_id = matching_companies[0].id
                return company_name, company_id
            else:
                return company_name, None
        else:
            for i, company in enumerate(matching_companies):
                click.echo(f'{i+1}. {company.name}')
            
            response = click.prompt('Voulez-vous sélectionner une entreprise parmi celles-ci? (O/N)', type=str)
            if response.upper() == 'O':
                selected_index = click.prompt('Sélectionnez l\'entreprise (entrez le numéro)', type=int)
                if 1 <= selected_index <= len(matching_companies):
                    selected_company = matching_companies[selected_index - 1]
                    company_id = selected_company.id
                    return selected_company.name, company_id
                else:
                    click.echo('Sélection invalide..')
                    return None, None
            else:
                return company_name, None
    else:
        click.echo("Aucune entreprise correspondante.")
        return None, None



def view_create_company(company_name):
    """
    Crée une nouvelle entreprise
    """
    new_company = []
    phone_number = None
    address = None
    industry = None

    click.echo(f"Création de l'entreprise {company_name}")
    response = click.prompt("Souhaitez-vous ajouter d'autres informations? (O/N) ")
    if response.upper() == "O":

        phone_number = click.prompt('Numéro de téléphone', type=str)
        while not is_valid_phone_number(phone_number):
            click.echo('Veuillez entrer un numéro de téléphone valide')
            phone_number = click.prompt('Numéro de téléphone', type=str)

        address = click.prompt('Adresse', type=str)
        while not all(c.isalnum() or c.isspace() for c in address):
            click.echo('Veuillez entrer une adresse valide')
            address = click.prompt('Adresse', type=str)

        industry = click.prompt('Secteur d\'activité', type=str)
        while not all(c.isalnum() or c.isspace() for c in industry):
            click.echo('Veuillez entrer une donnée valide')
            industry = click.prompt('Secteur d\'activité', type=str)

    new_company.extend([company_name, phone_number, address, industry])

    return new_company


