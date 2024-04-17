import click
from utils.input_validators import is_valid_email, is_valid_password



def view_login(checked, authorized):
    """
    Permet de tester l'email et le mot de passe, reçoit le token
    """
    if checked:
        if authorized:
            click.echo("Accès autorisé")
        else: 
            click.echo("Accès non autorisé")

    else:
        info_login = []
        click.echo('Veuillez entrer vos identifiants :')

        email = click.prompt('Votre email', type=str)
        while not is_valid_email(email):
            click.echo('Veuillez entrer un email valide')
            email = click.prompt('Email', type=str)
        info_login.append(email)

        password = click.prompt('Votre mot de passe', hide_input=True, type=str)
        while not is_valid_password(password):
            click.echo('Veuillez entrer un mot de passe valide')
        info_login.append(password)
            
        return info_login
