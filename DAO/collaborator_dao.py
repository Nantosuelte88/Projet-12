import jwt
import os
from models.clients import Client, Contract, Event
from models.collaboration import Collaborator, Department
from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker

from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker


class CollaboratorDAO:

    
    def get_all_collaborators():
        session = create_db_connection()
        try:
            collaborators = session.query(Collaborator).all()
            return collaborators
        finally:
            session.close()

    def get_collaborator(collaborator_id):
        session = create_db_connection()
        try:
            collaborator = session.query(Collaborator).get(collaborator_id)
            return collaborator
        finally:
            session.close()

    def create_collaborator(collaborator_data):
        session = create_db_connection()
        try:
            collaborator = Collaborator(**collaborator_data)
            session.add(collaborator)
            session.commit()
            return collaborator
        finally:
            session.close()

    def update_collaborator(collaborator_id, collaborator_data):
        session = create_db_connection()
        try:
            collaborator = session.query(Collaborator).get(collaborator_id)
            if not collaborator:
                return None
            for key, value in collaborator_data.items():
                if hasattr(collaborator, key):
                    setattr(collaborator, key, value)
            session.commit()
            return collaborator
        finally:
            session.close()

    def delete_collaborator(collaborator_id):
        session = create_db_connection()
        try:
            collaborator = session.query(Collaborator).get(collaborator_id)
            if not collaborator:
                return None
            session.delete(collaborator)
            session.commit()
            return collaborator
        finally:
            session.close()
