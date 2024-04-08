from models.clients import Client, Contract, Event
from models.collaboration import Collaborator, Department
from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker


engine = create_db_connection()
Session = sessionmaker(bind=engine)
session = Session()


def get_collaborator_by_id(collaborator_id):
    collaborator = session.query(Collaborator).get(collaborator_id)
    if not collaborator:
        return None
    return collaborator


def get_client_by_id(client_id):
    client = session.query(Client).get(client_id)
    if not client:
        return None
    return client


def get_contract_by_id(contract_id):
    contract = session.query(Contract).get(contract_id)
    if not contract:
        return None
    return contract
