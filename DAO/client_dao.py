import jwt
import os
from models.clients import Client, Contract, Event
from models.collaboration import Collaborator, Department
from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker

class ClientDAO:
    """
    DAO (Objet d'accès aux données) pour la gestion des clients.

    Cette classe fournit des méthodes pour interagir avec les données des clients dans la base de données.
    Elle permet de récupérer des clients, de créer de nouveaux clients, de mettre à jour les informations des clients
    et de supprimer des clients de la base de données.
    """

    def __init__(self, session):
        self.session = session

    def get_all_clients(self):
        clients = self.session.query(Client).all()
        return clients

    def get_client(client_id):
        session = create_db_connection()
        try:
            client = session.query(Client).get(client_id)
            if not client:
                return None
            return client
        finally:
            session.close()

    def create_client(client_data):
        session = create_db_connection()
        try:
            client = Client(**client_data)
            session.add(client)
            session.commit()
            return client
        finally:
            session.close()

    def update_client(client_id, client_data):
        session = create_db_connection()
        try:
            client = session.query(Client).get(client_id)
            if not client:
                return None
            for key, value in client_data.items():
                if hasattr(client, key):
                    setattr(client, key, value)
            session.commit()
            return client
        finally:
            session.close()

    def delete_client(client_id):
        session = create_db_connection()
        try:
            client = session.query(Client).get(client_id)
            if not client:
                return None
            session.delete(client)
            session.commit()
            return client
        finally:
            session.close()
