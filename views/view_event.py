import click
from utils.input_validators import is_valid_date_format
from controllers.department_crud import wich_collaborator_in_department
from controllers.client_crud import wich_client
from tabulate import tabulate
from utils.decorators import SUPPORT


def view_events(events, clients, supports):
    """
    Affiche les détails des événements.
    """
    if events:
        table_data = []

        for event, client, support in zip(events, clients, supports):

            row = [
                event.id,
                event.name,
                event.contract_id,
                client.full_name if client else "Client inconnu",
                f"{client.phone_number}\n{
                    client.email}" if client else "Client inconnu",
                event.date_start,
                event.date_end,
                support,
                event.location,
                event.attendees,
                event.notes
            ]
            table_data.append(row)

        headers = [" ", "Nom", "Contrat id", "Nom du client", "Contact du client", "Date de début",
                   "Date de fin", "Contact support chez Epic Event", "Lieu", "Nombres d'invités", "Commentaires"]
        print(tabulate(table_data, headers, tablefmt="grid"))
    else:
        print("Aucun événement à afficher")


def view_no_event_with_contract_unsigned(client, contract):
    click.echo(f'Le contrat n°{contract.id} du client {client.full_name}, n\'est pas signé. Vous ne pouvez pas créer d\'événement avec un contrat non signé')


def view_contract_has_event(contract, event):
    click.echo(f'L\'événement ~ {event.name} ~ existe deja pour le contrat n°{contract.id}. Vous devez supprimer ou modifier l\'événement existant ou choisir un autre contrat.')


def view_no_event_update_for_wrong_support(event):
    click.echo(f'Seul le collaborateur du département Support affilié à l\'événement ~ {event.name} ~ peut avoir accès à cette fonctionnalité.')


def view_create_event(client, contract, created):
    """
    Crée un nouvel événement pour un client sous contrat.
    """
    if created:
        click.echo('Nouvel événement crée avec succès')

    else:
        click.echo(f"Création d'un nouvel evenement pour le client {
                   client.full_name} sous contrat n°{contract.id}")

        new_event = []

        name = click.prompt('Nom de l\'événement', type=str)
        while not all(c.isalnum() or c.isspace() for c in name):
            click.echo('Veuillez entrer un nom valide')
            name = click.prompt('Nom de l\'événement', type=str)
        new_event.append(name)

        date_start = click.prompt('Date de début (AAAA-MM-JJ)', type=str)
        while not is_valid_date_format(date_start):
            click.echo('Veuillez entrer une date valide au format AAAA-MM-JJ')
            date_start = click.prompt('Date de début (AAAA-MM-JJ)', type=str)
        new_event.append(date_start)

        date_end = click.prompt('Date de fin (AAAA-MM-JJ)', type=str)
        while not is_valid_date_format(date_end):
            click.echo('Veuillez entrer une date valide au format AAAA-MM-JJ')
            date_end = click.prompt('Date de fin (AAAA-MM-JJ)', type=str)
        new_event.append(date_end)

        location = click.prompt('Le lieu de l\'événement', type=str)
        while not all(c.isalnum() or c.isspace() for c in location):
            click.echo('Veuillez entrer une donnée valide')
            location = click.prompt('Le lieu de l\'événement', type=str)
        new_event.append(location)

        attendees = click.prompt('Nombre de convives attendu', type=int)
        new_event.append(attendees)

        notes = click.prompt('Commentaire ', type=str)
        while not all(c.isalnum() or c.isspace() for c in notes):
            click.echo('Veuillez entrer une donnée valide')
            notes = click.prompt('Commentaire ', type=str)
        new_event.append(notes)

        response = click.prompt(
            'Voulez-vous ajouter un collaborateur du département support ? (O/N)', type=str)
        while response.upper() != 'O' and response.upper() != 'N':
            click.echo('Veuillez répondre par "O" pour Oui et "N" pour Non')
            response = click.prompt(
                'Voulez-vous ajouter un collaborateur du département support ? (O/N)', type=str)
        if response.upper() == 'O':
            collaborator_id = wich_collaborator_in_department(SUPPORT)
            click.echo(f'collabo : {collaborator_id}')
            if collaborator_id:
                collaborator = collaborator_id
            else:
                collaborator = None
        else:
            collaborator = None

        new_event.append(collaborator)

        return new_event


def view_search_event_by_name_or_client():
    """
    Permet de rechercher un événement par son nom ou par son client.
    """
    click.echo(
        'Souhaitez-vous retrouver l\'événement par son nom ou par son client ?')
    click.echo('1: Son nom')
    click.echo('2: Son client')
    choice = click.prompt('Entrez le numéro correspondant', type=int)
    if choice == 1:
        event_name = click.prompt(
            'Quel est le nom de l\'événement? ', type=str)
        if event_name:
            return {'name': event_name}
    if choice == 2:
        return {'client_name'}
    else:
        click.echo('Demande invalide')


def view_wich_event(events):
    """
    Affiche les événements trouvés et permet à l'utilisateur d'en sélectionner un.
    """
    if events:
        click.echo(f"Evénement.s trouvé.s :")
        for idx, event in enumerate(events, start=1):
            click.echo(f"{idx}. Nom de l\'événement {event.name}")

        selected_id = click.prompt(
            "Sélectionner le numéro de l'événement", type=int)

        if 1 <= selected_id <= len(events):
            selected_event = events[selected_id - 1]
            return selected_event
        else:
            click.echo("Numéro d'événement invalide.")
            return None
    else:
        click.echo("Aucun événement trouvé pour ce client")
        return None


def view_update_support_in_event(event, support, modified):
    """
    Affiche les informations sur la modification du collaborateur de support pour un événement donné.
    """
    if modified:
        click.echo("Evenement modifié avec succès")
    else:
        if support:
            click.echo(f"Modification du collaborateur {support.full_name} pour l'événement ~ {event.name} ~ ")
        else:
            click.echo(f"Ajout d'un collaborateur pour l'événement ~ {event.name} ~ ")

        collaborator_id = wich_collaborator_in_department(SUPPORT)
        if collaborator_id:
            event_data = {'support_id': collaborator_id}
            if event_data:
                return event_data
        else:
            click.echo('Demande annulée')


def view_update_event(event, client_name, modified):
    """
    Affiche les options de modification pour un événement donné et retourne les données mises à jour de l'événement.
    """
    if modified:
        click.echo("Evenement modifié avec succès")

    else:
        click.echo(
            f"Que souhaitez-vous modifier dans l'événement ~ {event.name} ~ de {client_name}")
        click.echo(f"1: Le nom : {event.name}")
        click.echo(f"2: La date de début : {event.date_start}")
        click.echo(f"3: La date de fin : {event.date_end}")
        click.echo(f"4: Le lieu de l'événement : {event.location}")
        click.echo(f"5: Le nombre de convives attendu : {event.attendees}")
        click.echo(f"6: Les commentaires : {event.notes}")
        click.echo(f"7: Le client associé : {client_name}")

        choice = click.prompt(
            "Entrez le numéro correspondant à votre choix: ", type=int)

        if choice == 1:
            new_name = click.prompt(
                "Entrez le nouveau nom de l'événement", type=str)
            while not all(c.isalnum() or c.isspace() for c in new_name):
                click.echo('Veuillez entrer un nom valide')
                new_name = click.prompt(
                    "Entrez le nouveau nom de l'événement", type=str)

            event_data = {'name': new_name}

        elif choice == 2:
            new_date_start = click.prompt(
                'Entrez la nouvelle date de début (AAAA-MM-JJ)', type=str)
            while not is_valid_date_format(new_date_start):
                click.echo(
                    'Veuillez entrer une date valide au format AAAA-MM-JJ')
                new_date_start = click.prompt(
                    'Date de début (AAAA-MM-JJ)', type=str)

            event_data = {'date_start': new_date_start}

        elif choice == 3:
            new_date_end = click.prompt(
                'Entrez la nouvelle date de fin (AAAA-MM-JJ)', type=str)
            while not is_valid_date_format(new_date_end):
                click.echo(
                    'Veuillez entrer une date valide au format AAAA-MM-JJ')
                new_date_end = click.prompt(
                    'Date de fin (AAAA-MM-JJ)', type=str)

            event_data = {'date_end': new_date_end}

        elif choice == 4:
            new_location = click.prompt(
                'Entrez le nouveau nom lieu de l\'événement', type=str)
            while not all(c.isalnum() or c.isspace() for c in new_location):
                click.echo('Veuillez entrer une donnée valide')
                new_location = click.prompt(
                    'Le lieu de l\'événement', type=str)

            event_data = {'location': new_location}

        elif choice == 5:
            new_attendees = click.prompt(
                'Entrez le nouveau nombre de convives attendu', type=int)
            event_data = {'attendees': new_attendees}

        elif choice == 6:
            new_notes = click.prompt('Commentaire ', type=str)
            while not all(c.isalnum() or c.isspace() for c in new_notes):
                click.echo('Veuillez entrer une donnée valide')
                new_notes = click.prompt('Commentaire ', type=str)

            event_data = {'notes': new_notes}

        elif choice == 7:
            new_client = wich_client()
            if new_client:
                click.echo(f'Le client {client_name} va être remplacé par le client {new_client.full_name} pour l\'événement ~ {event.name} ~')
                response = click.prompt(
                    'Confirmez-vous cette modification ? (O/N) ', type=str)
                if response.upper() == 'O':
                    contract_data = {'client_id': new_client.id}
                    return contract_data
                else:
                    click.echo('Modification annulée.')

        else:
            click.echo("Choix invalide.")
            return False

        return event_data


def view_delete_event(event, client, deleted):
    """
    Affiche le message de suppression d'un événement et retourne True si l'événement est supprimé, sinon False.
    """
    if deleted:
        click.echo('Evenement supprimé avec succès')
    else:
        click.echo(f'Suppresion de l\'événement ~ {event.name} ~ du client {client.full_name}')
        response = click.prompt(
            'Souhaitez-vous supprimer cet événement ? (O/N)')
        if response.upper() == 'O':
            return True
        else:
            click.echo('Suppression annulée')
            return False
