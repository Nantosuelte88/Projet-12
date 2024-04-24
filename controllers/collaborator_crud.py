import logging
from sentry_sdk import capture_message
from connect_database import create_db_connection
from DAO.collaborator_dao import CollaboratorDAO
from DAO.department_dao import DepartmentDAO
import bcrypt
from views.view_collaborator import view_all_collaborators, view_create_collaborator, view_update_collaborator, view_wich_collaborator, view_delete_collaborator
from utils.decorators import permission_for_gestion_department

logger = logging.getLogger(__name__)

session = create_db_connection()
collaborator_dao = CollaboratorDAO(session)
department_dao = DepartmentDAO(session)


def display_all_collaborators(token):
    """
    Affiche tous les colaborateurs de la base de données.
    """
    collaborators = collaborator_dao.get_all_collaborators()
    departments = []
    if collaborators:
        for collaborator in collaborators:
            department_name = department_dao.get_department(collaborator.department_id)
            if department_name:
                departments.append(department_name)
    
    view_all_collaborators(collaborators, departments)


@permission_for_gestion_department()
def create_collaborator():
    """
    Crée un nouveau collaborateur si l'utilisateur fait partie du département gestion.
    """
    created = False
    departments = department_dao.get_all_departments()
    info_collaborator = view_create_collaborator(created, departments)
    if info_collaborator:
        password = info_collaborator[2]
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        new_collaborator_data = {
            'full_name': info_collaborator[0],
            'email': info_collaborator[1],
            'password': hashed_password,
            'department_id': info_collaborator[3]
        }

        new_collaborator = collaborator_dao.create_collaborator(
            new_collaborator_data)

        if new_collaborator:
            created = True
            # Message pour Sentry
            message = f"Collaborator created: {new_collaborator.full_name}, {new_collaborator.email}"
            logger.info(message)
            capture_message(message)
            view_create_collaborator(created, departments)


@permission_for_gestion_department()
def update_collaborator(token):
    """
    Modifie un collaborateur si l'utilisateur fait partie du département gestion.
    """
    collaborator = wich_collaborator()
    departments = department_dao.get_all_departments()
    department = department_dao.get_department(collaborator.department_id)
    if collaborator:
        modified = False
        new_data = view_update_collaborator(
            collaborator, modified, departments, department)
        if new_data:
            modification = collaborator_dao.update_collaborator(
                collaborator.id, new_data)
            if modification:
                modified = True

                # Message pour Sentry
                message = f"Collaborator modified: {collaborator.full_name} ("
                if 'full_name' in new_data:
                    message += f"{new_data['full_name']} -> {collaborator.full_name}"
                else:
                    message += collaborator.full_name
                message += ")"
                logger.info(message)
                capture_message(message)

                # Envoie de la confirmation à la vue
                view_update_collaborator(
                    collaborator, modified, departments, department)


@permission_for_gestion_department()
def delete_collaborator(token):
    """
    Supprimer un collaborateur si l'utilisateur fait partie du département gestion.
    """
    collaborator = wich_collaborator()
    deleted = False
    if collaborator:
        response = view_delete_collaborator(collaborator, deleted)
        if response:
            remove = collaborator_dao.delete_collaborator(collaborator.id)
            if remove:
                deleted = True
                view_delete_collaborator(collaborator, deleted)


def wich_collaborator():
    """
    Renvoie une liste de collaborateurs dont le nom correspond à celui spécifié.
    """
    found = False
    collaborators_corresponding = None
    collaborator_name = view_wich_collaborator(
        collaborators_corresponding, found)
    if collaborator_name:
        collaborators_corresponding = collaborator_dao.get_corresponding_collaborator(
            collaborator_name)
        if collaborators_corresponding:
            found = True
            collaborator = view_wich_collaborator(
                collaborators_corresponding, found)
            if collaborator:
                return collaborator
