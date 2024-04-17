import click
import os
from dotenv import load_dotenv
from controllers.login import login


token_file_path = os.getenv('TOKEN_FILE_PATH')


@click.group()
def auth_commands():
    pass


@auth_commands.command()
@click.pass_context
def login_command(ctx):
    ctx.invoke(login)  # Appeler la commande Click login

    token = ctx.obj.get("token")  # Récupérer le token du contexte

    if token:
        # Écrire le token dans le fichier token.txt
        with open(token_file_path, "w") as file:
            file.write(token)



@auth_commands.command()
@click.pass_context
def logout_command(ctx):
    if "token" in ctx.obj:
        del ctx.obj["token"]

    with open(token_file_path, "w") as file:
        file.write("")

    click.echo("Vous avez été déconnecté.")

