import click
from controllers.auth_permissions import authenticate, authorize
from views.login import login
from models.clients import Client, Contract, Event
from models.collaboration import Collaborator, Department
from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker
from tabulate import tabulate
from utils.get_object import search_corresponding
from utils.decorators import department_permission_required
from utils.input_validators import is_valid_email, is_valid_phone_number


session = create_db_connection()


@click.command()
@click.option('--token', required=True, help='Le token d\'authentification')
@department_permission_required(3)
def view_create_user(token):
    """
    Crée un nouveau client
    """
    click.echo("Création d'un nouveau client :")

    new_client = []

    full_name = click.prompt('Nom complet', type=str)
    while not all(c.isalnum() or c.isspace() for c in full_name):
        click.echo('Veuillez entrer un nom complet valide')
        full_name = click.prompt('Nom complet', type=str)

    email = click.prompt('Email', type=str)
    while not is_valid_email(email):
        click.echo('Veuillez entrer un email valide')
        email = click.prompt('Email', type=str)

    phone_number = click.prompt('Numéro de téléphone', type=str)
    while not is_valid_phone_number(phone_number):
        click.echo('Veuillez entrer un numéro de téléphone valide')
        phone_number = click.prompt('Numéro de téléphone', type=str)

    response = click.prompt(
        'Voulez-vous entrer un nom d\'entreprise? (Y/N)', type=str)
    if response.upper() == 'Y':
        company_name = click.prompt('Nom de l\'entreprise', type=str)
        while not all(c.isalnum() or c.isspace() for c in company_name):
            click.echo(
                "Le nom de l'entreprise ne doit contenir que des chiffres, des lettres et des espaces.")
            company_name = click.prompt('Nom de l\'entreprise', type=str)
        new_client.append(company_name)
    else:
        new_client.append(None)

    new_client.extend([full_name, email, phone_number])

    return new_client
