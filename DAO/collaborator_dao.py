from models.collaboration import Collaborator


class CollaboratorDAO:
    """
    DAO (Objet d'accès aux données) pour la gestion des collaborateurs.
    """

    def __init__(self, session):
        self.session = session

    def get_all_collaborators(self):
        collaborators = self.session.query(Collaborator).all()
        return collaborators

    def get_collaborator(self, collaborator_id):
        collaborator = self.session.query(Collaborator).get(collaborator_id)
        return collaborator

    def get_corresponding_collaborator(self, collaborator_name):
        collaborators_names_min = self.session.query(Collaborator).filter(
            Collaborator.full_name.ilike(f"%{collaborator_name}%")).all()
        return collaborators_names_min

    def create_collaborator(self, collaborator_data):
        collaborator = Collaborator(**collaborator_data)
        self.session.add(collaborator)
        self.session.commit()
        return collaborator

    def update_collaborator(self, collaborator_id, collaborator_data):
        collaborator = self.session.query(Collaborator).get(collaborator_id)
        if not collaborator:
            return None
        for key, value in collaborator_data.items():
            if hasattr(collaborator, key):
                setattr(collaborator, key, value)
        self.session.commit()
        return collaborator

    def delete_collaborator(self, collaborator_id):
        collaborator = self.session.query(Collaborator).get(collaborator_id)
        if not collaborator:
            return None
        self.session.delete(collaborator)
        self.session.commit()
        return collaborator
