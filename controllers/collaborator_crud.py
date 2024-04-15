from connect_database import create_db_connection
from DAO.collaborator_dao import CollaboratorDAO
from DAO.department_dao import DepartmentDAO
import bcrypt
from datetime import datetime, timedelta, timezone
from views.view_collaborator import view_create_collaborator, view_update_collaborator, wich_collaborator, view_delete_collaborator


session = create_db_connection()
collaborator_dao = CollaboratorDAO(session)
department_dao = DepartmentDAO(session)

def create_collaborator(token):
    info_collaborator = view_create_collaborator()
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
            print('Nouveau collaborateur ajouté')
        else:
            print("Une erreur s'est produite.")


def update_collaborator(token):
    collaborator = wich_collaborator()
    if collaborator:
        modified = False
        new_data = view_update_collaborator(collaborator, modified)
        print(new_data)
        if new_data:
            modification = collaborator_dao.update_collaborator(collaborator.id, new_data)
            if modification:
                modified = True
                view_update_collaborator(collaborator, modified)
                
def delete_collaborator(token):
    collaborator = wich_collaborator()
    deleted = False
    response = view_delete_collaborator(collaborator, deleted)
    if response:
        remove = collaborator_dao.delete_collaborator(collaborator.id)
        if remove:
            deleted = True
            view_delete_collaborator(collaborator, deleted)
