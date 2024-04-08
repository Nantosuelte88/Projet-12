from controllers.auth_permissions import authenticate, authorize
from views.login import login
from models.clients import Client, Contract, Event
from models.collaboration import Collaborator, Department
from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker
from tabulate import tabulate
from utils.get_object import get_client_by_id, get_collaborator_by_id, get_contract_by_id
from utils.decorators import department_permission_required
from utils.input_validators import is_valid_email, is_valid_phone_number

session = create_db_connection()



@department_permission_required(3)
def view_create_user(token):
    print("Creation d'un nouveau client :")
    new_client = []
    while True:
        full_name = input('Nom complet: ')
        if all(c.isalnum() or c.isspace() for c in full_name):
            new_client.append(full_name)
            break
        else:
            print('Veuillez entrer un prénom valide')

    while True:
        email = input('Email: ')
        if is_valid_email(email):
            new_client.append(email)
            break
        else:
            print('Veuillez entrer un email valide')
    
    while True:
        phone_number = input('Numéro de téléphone: ')
        if is_valid_phone_number(phone_number):
            new_client.append(phone_number)
            break
        else:
            print('Veuillez entrer un numéro de téléphone valide')

    while True:
        response = input('Voulez-vous entrer un nom d\'entreprise? Y/N ')
        if response.upper() == 'Y':
            company_name = input('Nom de l\'entreprise: ')
            if all(c.isalnum() or c.isspace() for c in company_name):
                new_client.append(company_name)
                break
            else:
                print("Le nom de l'entreprise ne doit contenir que des chiffres, des lettres et des espaces.")
        elif response.upper() == 'N':
            new_client.append(None)
            break
    
    return new_client