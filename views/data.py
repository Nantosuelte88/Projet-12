from controllers.auth_permissions import authenticate, authorize
from views.login import login
from models.clients import Client, Contract, Event
from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker


engine = create_db_connection()
Session = sessionmaker(bind=engine)
session = Session()


def view_all_clients(token):
    if token:
        authorized = authorize(token)
        if authorized:
            # Récupérer tous les clients de la base de données
            clients = session.query(Client).all()
            
            # Afficher les informations des clients
            for client in clients:
                # if company_id:
                #     company = campany_id.name
                # afficher le nom du commercial plutot que son id
                print(f"Nom: {client.full_name}, \
                      Email: {client.email}, \
                      Téléphone: {client.phone_number}, \
                      Nome de l'entreprise: {client.company}, \
                      Date de création: {client.creation_date}, \
                      Dernier contact: {client.last_contact_date}, \
                      Contact commercial chez Epic Event: {client.commercial_id}")
        else:
            print("Accès non autorisé")
    else:
        print("Utilisateur non connecté")

def view_all_contracts(token):
    if token:
        authorized = authorize(token)
        if authorized:
            # Récupérer tous les contrats de la base de données
            contracts = session.query(Contract).all()
            
            # Afficher les informations des clients
            for contract in contracts:
                # faire 0 Non et 1 Oui pour le statut, verifier reste à payer (compta?)
                # recuperer infos du client
                print(f"Client: {contract.client_id}, \
                      Montant Total: {contract.total_amount}, \
                      Montant restant à payer: {contract.remaining_amount}, \
                      Date de création du contrat: {contract.creation_date}, \
                      Contrat signé: {contract.status}")
        else:
            print("Accès non autorisé")
    else:
        print("Utilisateur non connecté")

def view_all_events(token):
    if token:
        authorized = authorize(token)
        if authorized:
            # Récupérer tous les évenements de la base de données
            events = session.query(Event).all()
            
            # Afficher les informations des clients
            for event in events:
                print(f"Nom: {event.name}, \
                      ID de l'évéenement: {event.id}, \
                      Contrat ID: {event.contract_id}, \
                      Nom du client: {event.contract_id}, \
                      Contact du client: {event.contract_id}, \
                      Date de début: {event.date_start}, \
                      Date de fin: {event.date_end}, \
                      Contact support chez Epic Event: {event.support_id}, \
                      Lieu: {event.location}, \
                      Nombres d'invités: {event.attendees}, \
                      Commentaire: {event.notes}")
        else:
            print("Accès non autorisé")
    else:
        print("Utilisateur non connecté")