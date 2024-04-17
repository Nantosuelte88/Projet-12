import click
import os
from dotenv import load_dotenv
from views.login import login

token_file_path = os.getenv('TOKEN_FILE_PATH')


@click.group()
def login_commands():
    pass


@login_commands.command()
@click.pass_context
def login_command(ctx):
    ctx.invoke(login)  # Appeler la commande Click login

    token = ctx.obj.get("token")  # Récupérer le token du contexte

    if token:
        # Écrire le token dans le fichier token.txt
        with open(token_file_path, "w") as file:
            file.write(token)
        click.echo("Le token a été enregistré.")
    else:
        click.echo("Le token n'a pas été obtenu avec succès.")
