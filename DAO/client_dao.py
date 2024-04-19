from models.clients import Client


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

    def get_client(self, client_id):
        client = self.session.query(Client).get(client_id)
        return client

    def get_clients_by_name(self, client_name):
        clients = self.session.query(Client).filter(
            Client.full_name.ilike(f"%{client_name}%")).all()
        return clients

    def get_clients_by_collaborator_id(self, collaborator_id):
        clients = self.session.query(Client).filter_by(
            commercial_id=collaborator_id).all()
        return clients

    def create_client(self, client_data):
        client = Client(**client_data)
        for key, value in client_data.items():
            setattr(client, key, value)
        self.session.add(client)
        self.session.commit()
        return client

    def update_client(self, client_id, client_data):
        client = self.session.query(Client).get(client_id)
        if not client:
            return None
        for key, value in client_data.items():
            setattr(client, key, value)
        self.session.add(client)
        self.session.commit()
        return client

    def delete_client(self, client_id):
        client = self.session.query(Client).get(client_id)
        if not client:
            return None
        self.session.delete(client)
        self.session.commit()
        return client
