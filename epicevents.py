import click
import os
from controllers.auth_permissions import authenticate, authorize
from commands.client_commands import client_commands
from commands.collaborator_commands import collaborator_commands
from commands.contract_commands import contract_commands
from commands.event_commands import event_commands
from commands.login_logout_commands import auth_commands, token_file_path


@click.group()
@click.pass_context
def cli(ctx):
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

if __name__ == "__main__":
    cli()
