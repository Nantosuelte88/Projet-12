import click
import os
from dotenv import load_dotenv
from controllers.auth_permissions import authenticate, authorize
from views.login import login
from controllers.client_crud import display_all_clients, delete_client, display_my_clients, create_new_client, update_client
from controllers.contract_crud import display_all_contracts, display_contracts_unpaid, display_unsigned_contracts, create_contract, update_contract, delete_contract
from controllers.event_crud import display_all_events, display_event_without_support, display_my_events, create_event, update_event, delete_event
from controllers.collaborator_crud import create_collaborator, update_collaborator, delete_collaborator

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Définir le chemin vers le fichier de stockage du token
TOKEN_FILE_PATH = "token.txt"


@click.group()
@click.pass_context
def cli(ctx):
    # Vérifier si le token existe dans le fichier
    if os.path.exists(TOKEN_FILE_PATH):
        with open(TOKEN_FILE_PATH, "r") as file:
            token = file.read().strip()
        ctx.obj = {"token": token}
    else:
        ctx.obj = {"token": None}


@cli.command()
@click.pass_context
def login_command(ctx):
    ctx.invoke(login)  # Appeler la commande Click login

    token = ctx.obj.get("token")  # Récupérer le token du contexte

    if token:
        # Écrire le token dans le fichier token.txt
        with open(TOKEN_FILE_PATH, "w") as file:
            file.write(token)
        click.echo("Le token a été enregistré.")
    else:
        click.echo("Le token n'a pas été obtenu avec succès.")


@cli.command()
@click.pass_context
def prints_test(ctx):
    token = ctx.obj["token"]
    # Vérifier si le fichier existe
    if token:
        print(token)
        print("test?")
    else:
        print("Le fichier token.txt n'existe pas.")


# Clients = affichage, création, modification, suppresion
@cli.command()
@click.pass_context
def view_clients_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo("Veuillez vous connecter en utilisant la commande 'login' avant d'afficher les clients.")
        return
    display_all_clients(token)


@cli.command()
@click.pass_context
def view_my_clients_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant d'afficher les clients qui vous sont associés.")
        return
    display_my_clients(token)


@cli.command()
@click.pass_context
def create_user_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de créer un nouvel utilisateur.")
        return
    create_new_client(token)


@cli.command()
@click.pass_context
def update_client_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de modifier un utilisateur.")
        return
    update_client(token)

@cli.command()
@click.pass_context
def delete_client_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de supprimer un utilisateur.")
        return
    delete_client(token)


# Collaborateurs = création, modification, suppression
@cli.command()
@click.pass_context
def create_collaborator_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de créer un collaborateur.")
        return
    create_collaborator(token)


@cli.command()
@click.pass_context
def update_collaborator_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de modifier un collaborateur.")
        return
    update_collaborator(token)

@cli.command()
@click.pass_context
def delete_collaborator_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de supprimer un collaborateur.")
        return
    delete_collaborator(token)


# Contrats = affichage, création, modification et suppression
@cli.command()
@click.pass_context
def view_contracts_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant d'afficher les contrats.")
        return
    display_all_contracts(token)

@cli.command()
@click.pass_context
def create_contract_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de créer un contrat.")
        return
    create_contract(token)


@cli.command()
@click.pass_context
def update_contract_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de modifier un contrat.")
        return
    update_contract(token)

@cli.command()
@click.pass_context
def view_contracts_unpaid(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant d'afficher les contrats impayés.")
        return
    display_contracts_unpaid(token)


@cli.command()
@click.pass_context
def view_unsigned_contracts(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant d'afficher les contrats non signés.")
        return
    display_unsigned_contracts(token)


@cli.command()
@click.pass_context
def delete_contract_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de supprimer un contrat.")
        return
    delete_contract(token) 


# Evénement =affichage, création, modfication, suppression
@cli.command()
@click.pass_context
def view_events_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant d'afficher les événementss.")
        return
    display_all_events(token)

@cli.command()
@click.pass_context
def create_event_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de créer un événement.")
        return
    create_event(token)


@cli.command()
@click.pass_context
def update_event_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de modifier un événement.")
        return
    update_event(token)

@cli.command()
@click.pass_context
def event_without_support_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant d'afficher les événements sans support.")
        return
    display_event_without_support(token)

@cli.command()
@click.pass_context
def view_my_events_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant d'afficher les événements qui vous sont associés.")
        return
    display_my_events(token)


@cli.command()
@click.pass_context
def delete_event_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de supprimer un événement.")
        return
    delete_event(token)

if __name__ == "__main__":
    cli()
