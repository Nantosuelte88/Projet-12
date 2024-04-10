import click
import os
from dotenv import load_dotenv
from controllers.auth_permissions import authenticate, authorize
from views.login import login
from views.data import view_all_clients, view_all_contracts, view_all_events
from controllers.create_update import create_new_client

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


@cli.command()
@click.pass_context
def view_clients_command(ctx):
    token = ctx.obj["token"]

    if token is None:
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant d'afficher les clients.")
        return
    view_all_clients(token)


@cli.command()
@click.pass_context
def create_user_command(ctx):
    token = ctx.obj["token"]

    if token is None:
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de créer un nouvel utilisateur.")
        return
    create_new_client(token)


if __name__ == "__main__":
    cli()
