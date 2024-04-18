import click
from connect_database import create_db_connection
from tabulate import tabulate
from utils.input_validators import is_valid_email, is_valid_phone_number
from tabulate import tabulate
from controllers.company_crud import create_company
from views.view_company import wich_company


def view_clients(clients, collaborators):
    if clients:
        # Préparer les données pour le tableau
        table_data = []
        for client, collaborator in zip(clients, collaborators):
            row = [
                client.id,
                client.full_name,
                client.email,
                client.phone_number,
                client.company_name,
                client.creation_date,
                client.last_contact_date,
                collaborator.full_name if collaborator else "Commercial inconnu"
            ]
            table_data.append(row)

        # Afficher le tableau
        headers = [" ", "Nom", "Email", "Téléphone", "Nom de l'entreprise",
                   "Date de création", "Dernier contact", "Contact commercial chez Epic Event"]
        print(tabulate(table_data, headers, tablefmt="grid"))
    else:
        print("Aucun client à afficher")


def view_create_client(created):
    """
    Crée un nouveau client
    """
    if created:
        click.echo("Nouveau client enregistré avec succès")

    else:
        click.echo("Création d'un nouveau client :")

        new_client = []

        full_name = click.prompt('Nom complet', type=str)
        while not all(c.isalnum() or c.isspace() for c in full_name):
            click.echo('Veuillez entrer un nom complet valide')
            full_name = click.prompt('Nom complet', type=str)

        email = click.prompt('Email', type=str)
        while not is_valid_email(email):
            click.echo('Veuillez entrer un email valide')
            email = click.prompt('Email', type=str)

        phone_number = click.prompt('Numéro de téléphone', type=str)
        while not is_valid_phone_number(phone_number):
            click.echo('Veuillez entrer un numéro de téléphone valide')
            phone_number = click.prompt('Numéro de téléphone', type=str)

        response = click.prompt(
            'Voulez-vous entrer un nom d\'entreprise? (O/N)', type=str)
        if response.upper() == 'O':
            company_name = click.prompt('Nom de l\'entreprise', type=str)
            while not all(c.isalnum() or c.isspace() for c in company_name):
                click.echo(
                    "Le nom de l'entreprise ne doit contenir que des chiffres, des lettres et des espaces.")
                company_name = click.prompt('Nom de l\'entreprise', type=str)
            company_name, company_id = wich_company(company_name)
            if company_id is not None:
                click.echo("Le client sera créé avec l'entreprise associée")
                new_client.extend(
                    [full_name, email, phone_number, company_name, company_id])
            else:
                click.echo(
                    "Le client sera créé sans entreprise associée gkdfjgkvjfdc")
                new_client.extend(
                    [full_name, email, phone_number, company_name, None])
        else:
            click.echo("Le client sera créé sans entreprise associée")
            new_client.extend([full_name, email, phone_number, None, None])

        return new_client


def view_wich_client(clients_corresponding, found):
    if found:
        if clients_corresponding:
            if len(clients_corresponding) == 1:
                click.echo("Un client trouvé à ce nom")
                click.echo(clients_corresponding[0].full_name)
                response = click.prompt(
                    "Souhaitez-vous selectionner ce client ? (O/N)", type=str)
                if response.upper() == 'O':
                    return clients_corresponding[0]
                else:
                    click.echo('Selection annulée')
                    return None
            else:
                click.echo("Plusieurs clients correspondent à ce nom :")
                for idx, client in enumerate(clients_corresponding, start=1):
                    click.echo(f"{idx}. {client.full_name}")

                selected_idx = click.prompt(
                    "Entrez le numéro du client: ", type=int)
                if 1 <= selected_idx <= len(clients_corresponding):
                    return clients_corresponding[selected_idx - 1]
                else:
                    click.echo("Numéro de client invalide.")
                    return None
        else:
            click.echo("Aucun client correspondant.")
            return None
    else:
        client_name = click.prompt("Entrez le nom du client: ", type=str)
        return client_name


def view_update_client(client, modified):
    if modified:
        click.echo("Client modifié avec succès")
    else:
        response = click.prompt(
            f"Souhaitez-vous modifier {client.full_name} ? (O/N) ")

        if response.upper() == "O":
            click.echo("Que souhaitez-vous modifier ?")
            click.echo(f"1: Son nom complet : {client.full_name}")
            click.echo(f"2: Son email : {client.email}")
            click.echo(f"3: Son numéro de téléphone : {client.phone_number}")
            click.echo(f"4: Son entreprise : {
                       client.company or 'Actuellement vide'}")

            choice = click.prompt(
                "Entrez le numéro correspondant à votre choix: ", type=int)

            if choice == 1:
                new_full_name = click.prompt("Entrez le nouveau nom complet: ")
                while not all(c.isalnum() or c.isspace() for c in new_full_name):
                    click.echo('Veuillez entrer un nom complet valide')
                    new_full_name = click.prompt(
                        "Entrez le nouveau nom complet: ")
                client_data = {"full_name": new_full_name}

            elif choice == 2:
                new_email = click.prompt("Entrez le nouvel email: ")
                while not is_valid_email(new_email):
                    click.echo('Veuillez entrer un email valide')
                    new_email = click.prompt("Entrez le nouvel email: ")
                client_data = {"email": new_email}

            elif choice == 3:
                new_phone_number = click.prompt(
                    "Entrez le nouveau numéro de téléphone: ")
                while not is_valid_phone_number(new_phone_number):
                    click.echo('Veuillez entrer un numéro de téléphone valide')
                    new_phone_number = click.prompt(
                        "Entrez le nouveau numéro de téléphone: ")

                client_data = {"phone_number": new_phone_number}

            elif choice == 4:
                response = click.prompt(
                    'Voulez-vous entrer un nom d\'entreprise? (O/N)', type=str)
                if response.upper() == 'O':
                    new_company_name = click.prompt(
                        "Entrez le nom de la nouvelle entreprise: ")
                    while not all(c.isalnum() or c.isspace() for c in new_company_name):
                        click.echo(
                            "Le nom de l'entreprise ne doit contenir que des chiffres, des lettres et des espaces.")
                        new_company_name = click.prompt(
                            'Nom de l\'entreprise', type=str)
                    new_company_name, new_company_id = wich_company(
                        new_company_name)
                    if new_company_id is not None:
                        click.echo(
                            "Le client sera associé à la nouvelle entreprise")
                        client_data = {
                            "company_name": new_company_name, "company_id": new_company_id}
                    else:
                        click.echo(
                            "Le client sera créé sans entreprise associée")
                        client_data = {
                            "company_name": new_company_name, "company_id": None}
                else:
                    click.echo("Le client sera créé sans entreprise associée")
                    client_data = {"company_name": None, "company_id": None}

            else:
                click.echo("Choix invalide.")
                return False

            return client_data

        else:
            click.echo("Modification annulée.")
            return False


def view_delete_client(client, deleted, contracts):
    if deleted:
        click.echo('Client supprimé avec succès')
    elif contracts:
        click.echo(
            'Au moins un contrat est associé à ce client, vous  ne pouvez pas le supprimer actuellement')
    else:
        click.echo(f'Suppresion du client {client.full_name}')
        response = click.prompt('Souhaitez-vous supprimer ce client ? (O/N)')
        if response.upper() == 'O':
            return True
        else:
            click.echo('Suppression annulée')
            return False
        
