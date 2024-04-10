import jwt
import os
from models.clients import Client, Contract, Event
from models.collaboration import Collaborator, Department
from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker


class EventDAO:
    """
    DAO (Objet d'accès aux données) pour la gestion des événements.

    """

    def __init__(self, session):
        self.session = session

    def get_all_events(self):
        events = self.session.query(Event).all()
        return events

    def get_event(self, event_id):
        event = self.session.query(Event).get(event_id)
        if not event:
            return None
        return event

    def create_event(self, event_data):
        event = Event(**event_data)
        self.session.add(event)
        self.session.commit()
        return event

    def update_event(self, event_id, event_data):
        event = self.session.query(Event).get(event_id)
        if not event:
            return None
        for key, value in event_data.items():
            if hasattr(event, key):
                setattr(event, key, value)
        self.session.commit()
        return event

    def delete_event(self, event_id):
        event = self.session.query(Event).get(event_id)
        if not event:
            return None
        self.session.delete(event)
        self.session.commit()
        return event
