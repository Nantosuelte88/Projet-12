import jwt
import os
from models.clients import Client, Contract, Event
from models.collaboration import Collaborator, Department
from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker

from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker


class ContractDAO:
    """
    DAO (Objet d'accès aux données) pour la gestion des contrats.

    """

    def get_all_contracts():
        session = create_db_connection()
        try:
            contracts = session.query(Contract).all()
            return contracts
        finally:
            session.close()

    def get_contract(contract_id):
        session = create_db_connection()
        try:
            contract = session.query(Contract).get(contract_id)
            if not contract:
                return None
            return contract
        finally:
            session.close()

    def create_contract(contract_data):
        session = create_db_connection()
        try:
            contract = Contract(**contract_data)
            session.add(contract)
            session.commit()
            return contract
        finally:
            session.close()

    def update_contract(contract_id, contract_data):
        session = create_db_connection()
        try:
            contract = session.query(Contract).get(contract_id)
            if not contract:
                return None
            for key, value in contract_data.items():
                if hasattr(contract, key):
                    setattr(contract, key, value)
            session.commit()
            return contract
        finally:
            session.close()

    def delete_contract(contract_id):
        session = create_db_connection()
        try:
            contract = session.query(Contract).get(contract_id)
            if not contract:
                return None
            session.delete(contract)
            session.commit()
            return contract
        finally:
            session.close()
