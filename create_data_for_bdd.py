from connect_database import create_db_connection
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
import bcrypt
from models.collaboration import Collaborator, Department
from models.clients import Client, Contract, Event
from datetime import datetime, timedelta, timezone


engine = create_db_connection()

# Définissez la session SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()


def create_departments():
    # Création des départements
    departements = ['support', 'gestion', 'commercial']

    for dept in departements:
        department = Department(name=dept)
        session.add(department)

    # Valider les modifications et fermer la session
    session.commit()
    session.close()


def create_collaborator():
    # Définissez les informations pour créer le nouvel utilisateur
    full_name = "Emma Caréna"
    email = "emma.carena@epic_events.com"
    password = "password456"
    department_id = 3

    # Générez un sel (salt) aléatoire pour le hachage bcrypt
    salt = bcrypt.gensalt()

    # Hachez le mot de passe en utilisant bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Création d'un nouvel objet Collaborator avec les informations fournies et le mot de passe haché
    new_collaborator = Collaborator(
        full_name=full_name, email=email, password=hashed_password, department_id=department_id)

    # Ajoutez le nouvel objet Collaborator à la session SQLAlchemy et effectuez un commit
    session.add(new_collaborator)
    session.commit()


def create_client():
    # Définissez les valeurs des attributs pour le nouveau client
    full_name = "Mciehl Test"
    email = "michelt@tessst.com"
    phone_number = "0102030405"
    creation_date = datetime.now(timezone.utc)
    last_contact_date = None
    commercial_id = 4
    company_name = None
    company_id = None

    # Créez une instance du client avec les valeurs spécifiées
    new_client = Client(
        full_name=full_name,
        email=email,
        phone_number=phone_number,
        creation_date=creation_date,
        last_contact_date=last_contact_date,
        commercial_id=commercial_id,
        company_name=company_name,
        company_id=company_id
    )

    # Ajoutez le nouveau client à la session
    session.add(new_client)
    session.commit()


def create_contract():
    # Définissez les valeurs des attributs pour le nouveau client
    client_id = 1
    total_amount = 10000
    remaining_amount = 5000
    creation_date = datetime.now(timezone.utc)
    status = True

    # Créez une instance du client avec les valeurs spécifiées
    new_contract = Contract(
        client_id=client_id,
        total_amount=total_amount,
        remaining_amount=remaining_amount,
        creation_date=creation_date,
        status=status
    )

    # Ajoutez le nouveau client à la session
    session.add(new_contract)
    session.commit()


def create_events():
    # Définissez les valeurs des attributs pour le nouveau client
    name = "Test 1er event"
    contract_id = 1
    date_start = "2024-05-05"
    date_end = "2024-05-05"
    support_id = 2
    location = "Parc de sprinces"
    attendees = 500
    notes = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam in arcu eget turpis porta finibus."

    # Créez une instance du client avec les valeurs spécifiées
    new_client = Event(
        name=name,
        contract_id=contract_id,
        date_start=date_start,
        date_end=date_end,
        support_id=support_id,
        location=location,
        attendees=attendees,
        notes=notes
    )

    # Ajoutez le nouveau client à la session
    session.add(new_client)
    session.commit()


# create_departments()
# create_collaborator()
# create_client()
# create_contract()
#create_events()
session.close()
