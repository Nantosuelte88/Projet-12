import jwt
import os
from models.clients import Client, Contract, Event
from models.collaboration import Collaborator, Department
from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker


class ContractDAO:
    """
    DAO (Objet d'accès aux données) pour la gestion des contrats.

    """

    def __init__(self, session):
        self.session = session

    def get_all_contracts(self):
        contracts = self.session.query(Contract).all()
        return contracts

    def get_contract(self, contract_id):
        contract = self.session.query(Contract).get(contract_id)
        if not contract:
            return None
        return contract
    
    def get_contracts_by_client_id(self, client_id):
        contracts = self.session.query(Contract).filter_by(client_id=client_id).all()
        return contracts

    def create_contract(self, contract_data):
        contract = Contract(**contract_data)
        self.session.add(contract)
        self.session.commit()
        return contract

    def update_contract(self, contract_id, contract_data):
        contract = self.session.query(Contract).get(contract_id)
        if not contract:
            return None
        for key, value in contract_data.items():
            if hasattr(contract, key):
                setattr(contract, key, value)
        self.session.commit()
        return contract

    def delete_contract(self, contract_id):
        contract = self.session.query(Contract).get(contract_id)
        if not contract:
            return None
        self.session.delete(contract)
        self.session.commit()
        return contract
