from connect_database import create_db_connection
from DAO.collaborator_dao import CollaboratorDAO
from DAO.department_dao import DepartmentDAO
import bcrypt
from datetime import datetime, timedelta, timezone
from views.view_collaborator import view_create_collaborator, view_update_collaborator, view_wich_collaborator, view_delete_collaborator
from utils.decorators import permission_for_gestion_department


session = create_db_connection()
collaborator_dao = CollaboratorDAO(session)
department_dao = DepartmentDAO(session)

@permission_for_gestion_department()
def create_collaborator(token):
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

        new_collaborator = collaborator_dao.create_collaborator(new_collaborator_data)

        if new_collaborator:
            created = True
            view_create_collaborator(created, departments)

@permission_for_gestion_department()
def update_collaborator(token):
    collaborator = wich_collaborator()
    departments = department_dao.get_all_departments()
    department =  department_dao.get_department(collaborator.department_id)
    if collaborator:
        modified = False
        new_data = view_update_collaborator(collaborator, modified, departments, department)
        if new_data:
            modification = collaborator_dao.update_collaborator(collaborator.id, new_data)
            if modification:
                modified = True
                view_update_collaborator(collaborator, modified, departments, department)
                
@permission_for_gestion_department()
def delete_collaborator(token):
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
    found = False
    collaborators_corresponding = None
    collaborator_name = view_wich_collaborator(collaborators_corresponding, found)
    if collaborator_name:
        collaborators_corresponding = collaborator_dao.get_corresponding_collaborator(collaborator_name)
        if collaborators_corresponding:
            found = True
            collaborator = view_wich_collaborator(collaborators_corresponding, found)
            if collaborator:
                return collaborator

