import jwt
import os
from models.clients import Client, Contract, Event
from models.collaboration import Collaborator, Department
from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker

from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker


class EventtDAO:
    """
    DAO (Objet d'accès aux données) pour la gestion des événements.

    """

    def get_all_events():
        session = create_db_connection()
        try:
            events = session.query(Event).all()
            return events
        finally:
            session.close()

    def get_event(event_id):
        session = create_db_connection()
        try:
            event = session.query(Event).get(event_id)
            if not event:
                return None
            return event
        finally:
            session.close()

    def create_event(event_data):
        session = create_db_connection()
        try:
            event = Event(**event_data)
            session.add(event)
            session.commit()
            return event
        finally:
            session.close()

    def update_event(event_id, event_data):
        session = create_db_connection()
        try:
            event = session.query(Event).get(event_id)
            if not event:
                return None
            for key, value in event_data.items():
                if hasattr(event, key):
                    setattr(event, key, value)
            session.commit()
            return event
        finally:
            session.close()

    def delete_event(event_id):
        session = create_db_connection()
        try:
            event = session.query(Event).get(event_id)
            if not event:
                return None
            session.delete(event)
            session.commit()
            return event
        finally:
            session.close()
