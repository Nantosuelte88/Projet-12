import click
from connect_database import create_db_connection
from tabulate import tabulate
from utils.input_validators import is_valid_email, is_valid_phone_number, is_valid_password


def view_wich_collaborator(collaborators_corresponding, found):
    if found:
        if collaborators_corresponding:
            if len(collaborators_corresponding) == 1:
                click.echo("Un collaborateur trouvé à ce nom")
                click.echo(collaborators_corresponding[0].full_name)
                response = click.prompt("Souhaitez-vous selectionner ce collaborateur ? (O/N)", type=str)
                if response.upper() == 'O':
                    return collaborators_corresponding[0]
                else:
                    click.echo('Selection annulée')
                    return None
            
            else:
                click.echo('Plusieurs collaborateurs correspondent à ce nom:')
                for idx, collaborator in enumerate(collaborators_corresponding, start=1):
                    click.echo(f"{idx}. {collaborator.full_name}")
                
                selected_idx = click.prompt("Entrez le numéro du collaborateur: ", type=int)
                if 1 <= selected_idx <= len(collaborators_corresponding):
                    return collaborators_corresponding[selected_idx - 1]
                else:
                    click.echo("Numéro de collaborateur invalide.")
                    return None
        
        else:
            click.echo('Aucun collaborateur trouvé.')

    else:
        collaborator_name = click.prompt("Entrez le nom du collaborateur: ", type=str)
        return collaborator_name
         


def view_create_collaborator(created, departments):
    """
    Créer un nouveau collaborateur
    """
    if created:
        click.echo('Nouveau collaborateur ajouté avce succès')
    else:
        click.echo("Création d'un nouveau collaborateur :")

        new_collaborator = []

        if departments:

            full_name = click.prompt('Nom complet', type=str)
            while not all(c.isalnum() or c.isspace() for c in full_name):
                click.echo('Veuillez entrer un nom complet valide')
                full_name = click.prompt('Nom complet', type=str)
            new_collaborator.append(full_name)

            email = click.prompt('Email', type=str)
            while not is_valid_email(email):
                click.echo('Veuillez entrer un email valide')
                email = click.prompt('Email', type=str)
            new_collaborator.append(email)

            password = click.prompt('Mot de passe', hide_input=True, type=str)
            while not is_valid_password(password):
                click.echo('Veuillez entrer un mot de passe valide - A MODIFIER')
                password = click.prompt('Mot de passe', type=str)
            new_collaborator.append(password)
            
            click.echo('Choisissez un departement à associer :')
            for idx, department in enumerate(departments, start=1):
                click.echo(f"{idx}. {department.name}")    
            selected_department = click.prompt("Sélectionner lu numéro de departement", type=int)
            while not selected_department <=3:
                click.echo('Veuillez selectionner un numéro valide.')
                selected_department = click.prompt("Sélectionner lu numéro de departement", type=int)
            new_collaborator.append(selected_department)

            return new_collaborator

        else:
            click.echo("Une erreur s'est produite.")


def view_update_collaborator(collaborator, modified, departments):
    if modified:
        click.echo("Collaborateur modifié avec succès")

    else:
        response = click.prompt(f"Souhaitez-vous modifier {collaborator.full_name} ? (O/N)")

        if response.upper() == "O":
            click.echo("Que souhaitez-vous modifier ?")
            click.echo(f"1: Le nom complet : {collaborator.full_name}")
            click.echo(f"2: L'email : {collaborator.email}")
            click.echo(f"3: Le mot de passe ")
            click.echo(f"4: le departement associé : {collaborator.department_id}")

            choice = click.prompt(
                "Entrez le numéro correspondant à votre choix: ", type=int)

            if choice == 1:
                new_full_name = click.prompt("Entrez le nouveau nom complet: ")
                while not all(c.isalnum() or c.isspace() for c in new_full_name):
                    click.echo('Veuillez entrer un nom complet valide')
                    new_full_name = click.prompt('Nom complet', type=str)
                collaborator_data = {"full_name": new_full_name}

            elif choice == 2:
                new_email = click.prompt("Entrez le nouvel email: ")
                while not is_valid_email(new_email):
                    click.echo('Veuillez entrer un email valide')
                    new_email = click.prompt("Entrez le nouvel email: ")
                collaborator_data = {"email": new_email}

            elif choice == 3:
                new_password = click.prompt('Mot de passe', hide_input=True, type=str)
                while not is_valid_password(new_password):
                    click.echo('Veuillez entrer un mot de passe valide - A MODIFIER')
                    new_password = click.prompt('Mot de passe', type=str)
                collaborator_data = {'password': new_password}
            
            elif choice == 4:
                if departments:
                    click.echo('Choisissez un departement à associer :')
                    for idx, department in enumerate(departments, start=1):
                        click.echo(f"{idx}. {department.name}")    
                    selected_department = click.prompt("Sélectionner lu numéro de departement", type=int)
                    while not selected_department <=3:
                        click.echo('Veuillez selectionner un numéro valide.')
                        selected_department = click.prompt("Sélectionner lu numéro de departement", type=int)
                    collaborator_data = {'department_id': selected_department}
            
        
            else:
                click.echo("Choix invalide.")
                return False

            return collaborator_data
        
        else:
            click.echo("Modification annulée.")
            return False

def view_delete_collaborator(collaborator, deleted):
    if deleted:
        click.echo('Collaborateur supprimé avec succès')
    else:
        click.echo(f'Suppresion du collaborateur {collaborator.full_name}')
        response = click.prompt('Souhaitez-vous supprimer ce collaborateur ? (O/N)')
        if response.upper() == 'O':
            return True
        else:
            click.echo('Suppression annulée')
            return False
