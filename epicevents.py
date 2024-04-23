import sentry_sdk
from sentry_sdk import capture_exception
from sentry_sdk.integrations.flask import FlaskIntegration
import click
import os
from dotenv import load_dotenv
from commands.client_commands import client_commands
from commands.collaborator_commands import collaborator_commands
from commands.contract_commands import contract_commands
from commands.event_commands import event_commands
from commands.login_logout_commands import auth_commands, token_file_path

sentry_link = os.getenv('DSN')

sentry_sdk.init(
    dsn= sentry_link,
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


@click.group()
@click.pass_context
def cli(ctx):
    """
    Gère les différentes commandes de l'application.
    """
    # Vérifier si le token existe dans le fichier
    if os.path.exists(token_file_path):
        with open(token_file_path, "r") as file:
            token = file.read().strip()
        ctx.obj = {"token": token}
    else:
        ctx.obj = {"token": None}




# Ajouter les groupes de commandes
cli.add_command(auth_commands)
cli.add_command(client_commands)
cli.add_command(collaborator_commands)
cli.add_command(contract_commands)
cli.add_command(event_commands)


# Générer une division par zéro (erreur)
#result = 1 / 0


if __name__ == "__main__":
    try:
        cli()
    except Exception as e:
        capture_exception(e)
