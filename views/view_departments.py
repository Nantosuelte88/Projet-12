import click
from connect_database import create_db_connection
from tabulate import tabulate
from utils.input_validators import is_valid_email, is_valid_phone_number, is_valid_password
from DAO.client_dao import ClientDAO
from DAO.collaborator_dao import CollaboratorDAO
from DAO.department_dao import DepartmentDAO

session = create_db_connection()
collaborator_dao = CollaboratorDAO(session)
client_dao = ClientDAO(session)
department_dao = DepartmentDAO(session)



def wich_collaborator_in_department(department_id):
    collaborator_name = click.prompt("Entrez le nom du collaborateur: ")
    collaborator_found = None

    if collaborator_name.isalnum():
        collaborators_corresponding = collaborator_dao.get_corresponding_collaborator(collaborator_name)

        if collaborators_corresponding:
            if len(collaborators_corresponding) == 1:
                # Retourne le seul collaborateur trouvé
                click.echo(f'un collarateur correspondant {collaborators_corresponding[0].full_name}') 
                collaborator_found = collaborators_corresponding[0]
            else:
                click.echo("Plusieurs collaborateurs correspondent à ce nom :")
                for idx, collaborator in enumerate(collaborators_corresponding, start=1):
                    click.echo(f"{idx}. {collaborator.full_name}")

                selected_idx = click.prompt(
                    "Entrez le numéro du client: ", type=int)
                if 1 <= selected_idx <= len(collaborators_corresponding):
                    click.echo(f'{collaborators_corresponding[selected_idx - 1].full_name}')
                    collaborator_found = collaborators_corresponding[selected_idx - 1]

            # chercher departmeent
            if collaborator_found.department_id == department_id:
                return collaborator_found.id
            else:
                click.echo('Le collaborateur trouvé ne fait pas partie du departement demandé, aucun collaborateur ne sera ajouté')
                return None

        else:
            click.echo("Aucun client correspondant.")
            return None
        