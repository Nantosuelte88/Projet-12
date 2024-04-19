from models.clients import Event


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

    def get_events_by_name(self, event_name):
        events = self.session.query(Event).filter(
            Event.name.ilike(f"%{event_name}%")).all()
        return events

    def get_event_by_contract_id(self, contract_id):
        events = self.session.query(Event).filter_by(
            contract_id=contract_id).first()
        return events

    def get_events_by_collaborator_id(self, collaborator_id):
        events = self.session.query(Event).filter_by(
            support_id=collaborator_id).all()
        return events

    def get_events_without_support(self):
        events = self.session.query(Event).filter(
            Event.support_id.is_(None)).all()
        return events

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
