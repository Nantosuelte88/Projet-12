from connect_database import create_db_connection
from DAO.client_dao import ClientDAO
from DAO.collaborator_dao import CollaboratorDAO
from DAO.department_dao import DepartmentDAO
from views.view_departments import view_wich_collaborator_in_department

session = create_db_connection()
collaborator_dao = CollaboratorDAO(session)
client_dao = ClientDAO(session)
department_dao = DepartmentDAO(session)


def wich_collaborator_in_department(department_id):
    """
    Renvoie une liste de collaborateurs correspondant au département spécifié.
    """
    found = False
    collaborators_corresponding = None
    collaborator_name = view_wich_collaborator_in_department(
        collaborators_corresponding, department_id, found)
    if collaborator_name:
        collaborators_corresponding = collaborator_dao.get_corresponding_collaborator(
            collaborator_name)
        if collaborators_corresponding:
            collaborator = view_wich_collaborator_in_department(
                collaborators_corresponding, department_id, found)
            if collaborator:
                return collaborator
