import getpass
import click
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, timezone
from connect_database import create_db_connection
from models.collaboration import Collaborator
from controllers.auth_permissions import authenticate, authorize
from utils.input_validators import is_valid_email, is_valid_password


@click.command()
@click.pass_context
def login(ctx):
    """
    Permet de tester l'email et le mot de passe, reçoit le token
    """
    while True:
        click.echo('Veuillez entrer vos identifiants :')

        email = click.prompt('Votre email', type=str)
        if not is_valid_email(email):
            click.echo('Veuillez entrer un email valide')
            continue

        password = click.prompt('Votre mot de passe',
                                hide_input=True, type=str)
        if not is_valid_password(password):
            click.echo('Veuillez entrer un mot de passe valide')
            continue

        token = authenticate(email, password)

        if token:
            authorized = authorize(token, None)
            if authorized:
                click.echo("Accès autorisé")
                ctx.obj["token"] = token
                return
            else:
                click.echo("Accès non autorisé")
        else:
            click.echo("Échec de l'authentification")
